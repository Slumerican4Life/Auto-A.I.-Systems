"""
Test cases for the Content Generation Bot workflow.

This module contains test cases for the Content Generation Bot workflow.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from workflows.content_generation.service import ContentGenerationService

# Mock data
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
    'workflow_type': 'content_generation',
    'active': True,
    'settings': {
        'blog_post': {
            'target_audience': 'Small to medium-sized businesses',
            'brand_voice': 'professional',
            'word_count': 800,
            'keywords': 'software development, custom solutions, business growth',
            'call_to_action': 'Contact us for a free consultation'
        },
        'social_media': {
            'target_audience': 'Small to medium-sized businesses',
            'brand_voice': 'conversational',
            'hashtags': '#software #development #business',
            'call_to_action': 'Visit our website'
        },
        'email_newsletter': {
            'target_audience': 'Existing clients and prospects',
            'brand_voice': 'friendly',
            'newsletter_type': 'monthly update',
            'content_sections': 'company news, industry insights, tips',
            'primary_goal': 'nurture relationships',
            'call_to_action': 'Schedule a call',
            'word_count': 500
        },
        'product_description': {
            'target_audience': 'Potential customers',
            'brand_voice': 'professional',
            'word_count': 300,
            'keywords': 'software solution, custom development'
        },
        'publishing': {
            'wordpress': {
                'api_url': 'https://example.com/wp-json/wp/v2',
                'username': 'admin',
                'password': 'password'
            },
            'buffer': {
                'api_key': 'buffer-api-key'
            },
            'mailchimp': {
                'api_key': 'mailchimp-api-key',
                'list_id': 'list-123'
            }
        }
    }
}

mock_workflow_run = {
    'id': 'workflow-run-123',
    'company_id': 'company-123',
    'workflow_config_id': 'workflow-123',
    'status': 'running',
    'started_at': datetime.now(),
    'trigger_type': 'manual',
    'actions_performed': [],
    'results': {}
}

mock_content = {
    'id': 'content-123',
    'company_id': 'company-123',
    'type': 'blog_post',
    'title': 'How Custom Software Can Boost Your Business',
    'content': 'This is a sample blog post content...',
    'topic': 'custom software',
    'status': 'draft',
    'metadata': {
        'word_count': 800,
        'keywords': 'software development, custom solutions, business growth',
        'title_options': '1. How Custom Software Can Boost Your Business\n2. 5 Ways Custom Software Drives Business Growth\n3. The Business Case for Custom Software Development\n4. Why Your Business Needs Custom Software Solutions\n5. Transforming Your Business with Custom Software'
    },
    'created_at': datetime.now(),
    'updated_at': datetime.now(),
    'workflow_run_id': 'workflow-run-123'
}

@pytest.fixture
def content_generation_service():
    """Create a ContentGenerationService instance with mocked dependencies."""
    service = ContentGenerationService()
    service.ai_service = MagicMock()
    service.email_service = MagicMock()
    return service

@pytest.mark.asyncio
async def test_generate_blog_post_success(content_generation_service):
    """Test generating a blog post successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.return_value = mock_company
        mock_query_collection.return_value = [mock_workflow_config]
        mock_create_document.side_effect = [mock_workflow_run, mock_content]
        
        # Mock AI service
        content_generation_service.ai_service.generate_text.side_effect = [
            '1. How Custom Software Can Boost Your Business\n2. 5 Ways Custom Software Drives Business Growth\n3. The Business Case for Custom Software Development\n4. Why Your Business Needs Custom Software Solutions\n5. Transforming Your Business with Custom Software',
            'This is a sample blog post content...'
        ]
        
        # Call the method
        result = await content_generation_service.generate_blog_post('company-123', 'custom software')
        
        # Assertions
        assert result['success'] is True
        assert 'content_id' in result
        assert 'title' in result
        assert 'content' in result
        assert 'title_options' in result
        mock_get_document.assert_called_once_with('companies', 'company-123')
        mock_query_collection.assert_called_once()
        assert mock_create_document.call_count == 2
        mock_update_document.assert_called_once()
        assert content_generation_service.ai_service.generate_text.call_count == 2

@pytest.mark.asyncio
async def test_generate_social_media_post_success(content_generation_service):
    """Test generating a social media post successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.return_value = mock_company
        mock_query_collection.return_value = [mock_workflow_config]
        
        social_media_content = mock_content.copy()
        social_media_content['type'] = 'social_media'
        social_media_content['title'] = 'LinkedIn Post: custom software'
        social_media_content['metadata'] = {
            'platform': 'linkedin',
            'character_count': 200,
            'hashtags': '#software #development #business'
        }
        
        mock_create_document.side_effect = [mock_workflow_run, social_media_content]
        
        # Mock AI service
        content_generation_service.ai_service.generate_text.return_value = 'This is a sample social media post content...'
        
        # Call the method
        result = await content_generation_service.generate_social_media_post('company-123', 'custom software', 'linkedin')
        
        # Assertions
        assert result['success'] is True
        assert 'content_id' in result
        assert 'title' in result
        assert 'content' in result
        mock_get_document.assert_called_once_with('companies', 'company-123')
        mock_query_collection.assert_called_once()
        assert mock_create_document.call_count == 2
        mock_update_document.assert_called_once()
        content_generation_service.ai_service.generate_text.assert_called_once()

@pytest.mark.asyncio
async def test_generate_email_newsletter_success(content_generation_service):
    """Test generating an email newsletter successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.return_value = mock_company
        mock_query_collection.return_value = [mock_workflow_config]
        
        email_newsletter_content = mock_content.copy()
        email_newsletter_content['type'] = 'email_newsletter'
        email_newsletter_content['title'] = 'Your Monthly Update from Acme Inc.'
        email_newsletter_content['metadata'] = {
            'newsletter_type': 'monthly update',
            'word_count': 500,
            'subject_line_options': '1. Your Monthly Update from Acme Inc.\n2. This Month in Tech: Insights from Acme Inc.\n3. Acme Inc. Monthly Newsletter: Tech Trends & Updates\n4. Stay Informed: Your Monthly Tech Briefing\n5. The Acme Inc. Monthly Digest: Tech News & Tips'
        }
        
        mock_create_document.side_effect = [mock_workflow_run, email_newsletter_content]
        
        # Mock AI service
        content_generation_service.ai_service.generate_text.side_effect = [
            '1. Your Monthly Update from Acme Inc.\n2. This Month in Tech: Insights from Acme Inc.\n3. Acme Inc. Monthly Newsletter: Tech Trends & Updates\n4. Stay Informed: Your Monthly Tech Briefing\n5. The Acme Inc. Monthly Digest: Tech News & Tips',
            'This is a sample email newsletter content...'
        ]
        
        # Call the method
        result = await content_generation_service.generate_email_newsletter('company-123', 'monthly update')
        
        # Assertions
        assert result['success'] is True
        assert 'content_id' in result
        assert 'title' in result
        assert 'content' in result
        assert 'subject_line_options' in result
        mock_get_document.assert_called_once_with('companies', 'company-123')
        mock_query_collection.assert_called_once()
        assert mock_create_document.call_count == 2
        mock_update_document.assert_called_once()
        assert content_generation_service.ai_service.generate_text.call_count == 2

@pytest.mark.asyncio
async def test_generate_product_description_success(content_generation_service):
    """Test generating a product description successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.return_value = mock_company
        mock_query_collection.return_value = [mock_workflow_config]
        
        product_description_content = mock_content.copy()
        product_description_content['type'] = 'product_description'
        product_description_content['title'] = 'Custom CRM Solution'
        product_description_content['metadata'] = {
            'product_category': 'CRM',
            'word_count': 300,
            'platform': 'website'
        }
        
        mock_create_document.side_effect = [mock_workflow_run, product_description_content]
        
        # Mock AI service
        content_generation_service.ai_service.generate_text.return_value = 'This is a sample product description content...'
        
        # Call the method
        result = await content_generation_service.generate_product_description(
            'company-123',
            'Custom CRM Solution',
            product_category='CRM',
            key_features='Contact management, Sales pipeline, Reporting',
            primary_benefits='Increased productivity, Better customer insights',
            technical_specifications='Cloud-based, Mobile app, API integration',
            price_point='Starting at $99/month',
            unique_selling_proposition='Fully customizable to your business processes'
        )
        
        # Assertions
        assert result['success'] is True
        assert 'content_id' in result
        assert 'title' in result
        assert 'content' in result
        mock_get_document.assert_called_once_with('companies', 'company-123')
        mock_query_collection.assert_called_once()
        assert mock_create_document.call_count == 2
        mock_update_document.assert_called_once()
        content_generation_service.ai_service.generate_text.assert_called_once()

@pytest.mark.asyncio
async def test_schedule_content_generation_success(content_generation_service):
    """Test scheduling content generation successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document:
        
        # Set up mock returns
        mock_get_document.return_value = mock_company
        mock_query_collection.side_effect = [
            [mock_workflow_config],  # First call for workflow configs
            []  # Second call for existing schedules
        ]
        
        mock_create_document.return_value = {
            'id': 'schedule-123',
            'company_id': 'company-123',
            'content_type': 'blog_post',
            'frequency': 'weekly',
            'day_of_week': 'Monday',
            'time_of_day': '09:00',
            'topics': ['software development', 'business growth', 'technology trends'],
            'parameters': {
                'word_count': 800,
                'call_to_action': 'Contact us for a free consultation'
            },
            'active': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Call the method
        result = await content_generation_service.schedule_content_generation(
            'company-123',
            {
                'content_type': 'blog_post',
                'frequency': 'weekly',
                'day_of_week': 'Monday',
                'time_of_day': '09:00',
                'topics': ['software development', 'business growth', 'technology trends'],
                'parameters': {
                    'word_count': 800,
                    'call_to_action': 'Contact us for a free consultation'
                },
                'active': True
            }
        )
        
        # Assertions
        assert result['success'] is True
        assert 'schedule_id' in result
        mock_get_document.assert_called_once_with('companies', 'company-123')
        assert mock_query_collection.call_count == 2
        mock_create_document.assert_called_once()

@pytest.mark.asyncio
async def test_publish_content_success(content_generation_service):
    """Test publishing content successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('contents', 'content-123'): mock_content,
            ('companies', 'company-123'): mock_company,
            ('workflow_runs', 'workflow-run-123'): mock_workflow_run
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = [mock_workflow_config]
        
        # Call the method
        result = await content_generation_service.publish_content('content-123', 'wordpress')
        
        # Assertions
        assert result['success'] is True
        assert 'content_id' in result
        assert 'platform' in result
        assert 'url' in result
        mock_get_document.assert_any_call('contents', 'content-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_query_collection.assert_called_once()
        assert mock_update_document.call_count == 2

