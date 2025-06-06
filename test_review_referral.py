"""
Test cases for the Review & Referral Generator workflow.

This module contains test cases for the Review & Referral Generator workflow.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from workflows.review_referral.service import ReviewReferralService

# Mock data
mock_sale = {
    'id': 'sale-123',
    'company_id': 'company-123',
    'customer_id': 'customer-123',
    'amount': 199.99,
    'status': 'completed',
    'date': datetime.now() - timedelta(days=1),
    'products': [
        {'id': 'product-123', 'name': 'Premium Package', 'price': 199.99}
    ]
}

mock_customer = {
    'id': 'customer-123',
    'company_id': 'company-123',
    'name': 'Jane Smith',
    'email': 'jane.smith@example.com',
    'phone': '+1234567890',
    'created_at': datetime.now() - timedelta(days=30)
}

mock_company = {
    'id': 'company-123',
    'name': 'Acme Inc.',
    'industry': 'Technology',
    'settings': {
        'products_services': 'Software development, IT consulting',
        'value_proposition': 'We help businesses grow with custom software solutions'
    }
}

mock_workflow_config = {
    'id': 'workflow-123',
    'company_id': 'company-123',
    'workflow_type': 'review_referral',
    'active': True,
    'actions': {
        'initial_delay_hours': 48,
        'review_platforms': ['google', 'yelp'],
        'referral_offer': {
            'referrer_offer': '10% off next purchase',
            'description': '$20 off for new customers',
            'expiration_days': 30
        }
    },
    'settings': {
        'review_links': {
            'google': 'https://g.page/r/acme-inc/review',
            'yelp': 'https://www.yelp.com/biz/acme-inc/review'
        }
    },
    'templates': {
        'review_request': 'Hi {{customer_name}}, thank you for your recent purchase. We would appreciate your feedback.',
        'referral_offer': 'Hi {{customer_name}}, thank you for your review. Here is your referral code: {{referral_code}}.',
        'referral_reminder': 'Hi {{customer_name}}, just a reminder about your referral code: {{referral_code}}.'
    }
}

mock_workflow_run = {
    'id': 'workflow-run-123',
    'company_id': 'company-123',
    'workflow_config_id': 'workflow-123',
    'status': 'running',
    'started_at': datetime.now(),
    'trigger_type': 'sale_completed',
    'trigger_id': 'sale-123',
    'actions_performed': [],
    'results': {}
}

mock_review = {
    'id': 'review-123',
    'company_id': 'company-123',
    'customer_id': 'customer-123',
    'sale_id': 'sale-123',
    'rating': None,
    'content': None,
    'platform': None,
    'status': 'requested',
    'request_sent_at': None,
    'submitted_at': None,
    'verified_at': None,
    'created_at': datetime.now(),
    'updated_at': datetime.now()
}

mock_referral = {
    'id': 'referral-123',
    'company_id': 'company-123',
    'customer_id': 'customer-123',
    'review_id': 'review-123',
    'code': 'ACME123',
    'status': 'created',
    'offer': {
        'referrer_offer': '10% off next purchase',
        'description': '$20 off for new customers'
    },
    'created_at': datetime.now(),
    'updated_at': datetime.now(),
    'expires_at': datetime.now() + timedelta(days=30)
}

@pytest.fixture
def review_referral_service():
    """Create a ReviewReferralService instance with mocked dependencies."""
    service = ReviewReferralService()
    service.ai_service = MagicMock()
    service.email_service = MagicMock()
    return service

@pytest.mark.asyncio
async def test_process_completed_sale_success(review_referral_service):
    """Test processing a completed sale successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('sales', 'sale-123'): mock_sale,
            ('customers', 'customer-123'): mock_customer,
            ('companies', 'company-123'): mock_company
        }.get((collection, doc_id))
        
        mock_query_collection.side_effect = lambda collection, **kwargs: {
            'workflow_configs': [mock_workflow_config],
            'reviews': []
        }.get(collection)
        
        mock_create_document.side_effect = [mock_workflow_run, mock_review]
        
        # Call the method
        result = await review_referral_service.process_completed_sale('sale-123')
        
        # Assertions
        assert result['success'] is True
        assert 'review_id' in result
        assert 'workflow_run_id' in result
        assert 'scheduled_for' in result
        mock_get_document.assert_any_call('sales', 'sale-123')
        mock_get_document.assert_any_call('customers', 'customer-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        assert mock_query_collection.call_count == 2
        assert mock_create_document.call_count == 2
        mock_update_document.assert_called_once()

@pytest.mark.asyncio
async def test_process_completed_sale_not_completed(review_referral_service):
    """Test processing a sale that is not completed."""
    # Create a non-completed sale
    non_completed_sale = mock_sale.copy()
    non_completed_sale['status'] = 'pending'
    
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document:
        # Set up mock returns
        mock_get_document.return_value = non_completed_sale
        
        # Call the method
        result = await review_referral_service.process_completed_sale('sale-123')
        
        # Assertions
        assert result['success'] is False
        assert 'Sale is not completed' in result['message']
        mock_get_document.assert_called_once_with('sales', 'sale-123')

@pytest.mark.asyncio
async def test_send_review_request_success(review_referral_service):
    """Test sending a review request successfully."""
    # Create a review with no request_sent_at
    review = mock_review.copy()
    
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('reviews', 'review-123'): review,
            ('customers', 'customer-123'): mock_customer,
            ('companies', 'company-123'): mock_company,
            ('sales', 'sale-123'): mock_sale
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = [mock_workflow_config]
        
        # Mock AI service
        review_referral_service.ai_service.generate_text.return_value = "Generated review request"
        
        # Mock email service
        review_referral_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await review_referral_service.send_review_request('review-123')
        
        # Assertions
        assert result['success'] is True
        assert 'review_id' in result
        mock_get_document.assert_any_call('reviews', 'review-123')
        mock_get_document.assert_any_call('customers', 'customer-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_get_document.assert_any_call('sales', 'sale-123')
        mock_query_collection.assert_called_once()
        mock_update_document.assert_called_once()
        review_referral_service.ai_service.generate_text.assert_called()
        review_referral_service.email_service.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_process_submitted_review_success(review_referral_service):
    """Test processing a submitted review successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('reviews', 'review-123'): mock_review,
            ('customers', 'customer-123'): mock_customer,
            ('companies', 'company-123'): mock_company
        }.get((collection, doc_id))
        
        mock_query_collection.side_effect = lambda collection, **kwargs: {
            'workflow_configs': [mock_workflow_config],
            'workflow_runs': [mock_workflow_run]
        }.get(collection)
        
        mock_create_document.return_value = mock_referral
        
        # Mock AI service
        review_referral_service.ai_service.generate_text.return_value = "Generated referral offer"
        
        # Mock email service
        review_referral_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await review_referral_service.process_submitted_review('review-123', 5, 'Great service!', 'google')
        
        # Assertions
        assert result['success'] is True
        assert 'review_id' in result
        assert 'referral_id' in result
        assert 'referral_code' in result
        mock_get_document.assert_any_call('reviews', 'review-123')
        mock_get_document.assert_any_call('customers', 'customer-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        assert mock_query_collection.call_count == 2
        mock_create_document.assert_called_once()
        assert mock_update_document.call_count == 2
        review_referral_service.ai_service.generate_text.assert_called()
        review_referral_service.email_service.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_send_referral_reminder_success(review_referral_service):
    """Test sending a referral reminder successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('referrals', 'referral-123'): mock_referral,
            ('customers', 'customer-123'): mock_customer,
            ('companies', 'company-123'): mock_company,
            ('workflow_runs', 'workflow-run-123'): mock_workflow_run,
            ('workflow_configs', 'workflow-123'): mock_workflow_config
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = [mock_workflow_run]
        
        # Mock AI service
        review_referral_service.ai_service.generate_text.return_value = "Generated referral reminder"
        
        # Mock email service
        review_referral_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await review_referral_service.send_referral_reminder('referral-123')
        
        # Assertions
        assert result['success'] is True
        assert 'referral_id' in result
        mock_get_document.assert_any_call('referrals', 'referral-123')
        mock_get_document.assert_any_call('customers', 'customer-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_query_collection.assert_called_once()
        mock_update_document.assert_called_once()
        review_referral_service.ai_service.generate_text.assert_called()
        review_referral_service.email_service.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_process_referral_use_success(review_referral_service):
    """Test processing a referral use successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('leads', 'lead-123'): {'id': 'lead-123', 'name': 'New Lead'},
            ('customers', 'customer-123'): mock_customer,
            ('companies', 'company-123'): mock_company,
            ('workflow_runs', 'workflow-run-123'): mock_workflow_run
        }.get((collection, doc_id))
        
        mock_query_collection.side_effect = lambda collection, **kwargs: {
            'referrals': [mock_referral],
            'workflow_runs': [mock_workflow_run]
        }.get(collection)
        
        # Mock email service
        review_referral_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await review_referral_service.process_referral_use('ACME123', 'lead-123')
        
        # Assertions
        assert result['success'] is True
        assert 'referral_id' in result
        assert 'lead_id' in result
        mock_get_document.assert_any_call('leads', 'lead-123')
        mock_get_document.assert_any_call('customers', 'customer-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        assert mock_query_collection.call_count == 2
        mock_create_document.assert_called_once()
        assert mock_update_document.call_count == 2
        review_referral_service.email_service.send_email.assert_called_once()

