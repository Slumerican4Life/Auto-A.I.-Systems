"""
Test cases for the Lead Nurturing Agent workflow.

This module contains test cases for the Lead Nurturing Agent workflow.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime

from workflows.lead_nurturing.service import LeadNurturingService

# Mock data
mock_lead = {
    'id': 'lead-123',
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'phone': '+1234567890',
    'company_id': 'company-123',
    'source': 'website_form',
    'status': 'new',
    'notes': 'Interested in your services',
    'created_at': datetime.now(),
    'updated_at': datetime.now()
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
    'workflow_type': 'lead_nurturing',
    'active': True,
    'actions': {
        'channel': 'email',
        'message_template': 'initial_contact',
        'follow_up': [
            {
                'delay_hours': 24,
                'message_template': 'follow_up_1'
            },
            {
                'delay_hours': 72,
                'message_template': 'follow_up_2'
            }
        ]
    },
    'templates': {
        'initial_contact': 'Hi {{lead_name}}, thanks for your interest in {{business_name}}.',
        'follow_up_1': 'Hi {{lead_name}}, just following up on your interest in {{business_name}}.',
        'follow_up_2': 'Hi {{lead_name}}, this is our final follow-up regarding your interest in {{business_name}}.'
    },
    'triggers': {
        'lead_source': ['website_form', 'manual_entry', 'ad_campaign']
    }
}

mock_workflow_run = {
    'id': 'workflow-run-123',
    'company_id': 'company-123',
    'workflow_config_id': 'workflow-123',
    'status': 'running',
    'started_at': datetime.now(),
    'trigger_type': 'new_lead',
    'trigger_id': 'lead-123',
    'actions_performed': [],
    'results': {}
}

mock_interaction = {
    'id': 'interaction-123',
    'company_id': 'company-123',
    'lead_id': 'lead-123',
    'type': 'email',
    'direction': 'outbound',
    'content': 'Hi John, thanks for your interest in Acme Inc.',
    'channel': 'automated_workflow',
    'status': 'delivered',
    'created_at': datetime.now(),
    'metadata': {
        'subject': 'Thanks for your interest in Acme Inc.',
        'workflow_run_id': 'workflow-run-123'
    }
}

@pytest.fixture
def lead_nurturing_service():
    """Create a LeadNurturingService instance with mocked dependencies."""
    service = LeadNurturingService()
    service.ai_service = MagicMock()
    service.email_service = MagicMock()
    service.sms_service = MagicMock()
    return service

@pytest.mark.asyncio
async def test_process_new_lead_success(lead_nurturing_service):
    """Test processing a new lead successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('leads', 'lead-123'): mock_lead,
            ('companies', 'company-123'): mock_company
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = [mock_workflow_config]
        mock_create_document.return_value = mock_workflow_run
        
        # Mock AI service
        lead_nurturing_service.ai_service.generate_text.return_value = "Generated message"
        
        # Mock email service
        lead_nurturing_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await lead_nurturing_service.process_new_lead('lead-123')
        
        # Assertions
        assert result['success'] is True
        assert 'workflow_run_id' in result
        mock_get_document.assert_any_call('leads', 'lead-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_query_collection.assert_called_once()
        mock_create_document.assert_called()
        mock_update_document.assert_called()
        lead_nurturing_service.email_service.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_process_new_lead_no_workflow(lead_nurturing_service):
    """Test processing a new lead with no active workflow."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('leads', 'lead-123'): mock_lead,
            ('companies', 'company-123'): mock_company
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = []  # No active workflow
        
        # Call the method
        result = await lead_nurturing_service.process_new_lead('lead-123')
        
        # Assertions
        assert result['success'] is False
        assert 'No active workflow found' in result['message']
        mock_get_document.assert_any_call('leads', 'lead-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_query_collection.assert_called_once()

@pytest.mark.asyncio
async def test_process_follow_up_success(lead_nurturing_service):
    """Test processing a follow-up successfully."""
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('leads', 'lead-123'): mock_lead,
            ('companies', 'company-123'): mock_company,
            ('workflow_runs', 'workflow-run-123'): mock_workflow_run,
            ('workflow_configs', 'workflow-123'): mock_workflow_config
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = []  # No replies
        mock_create_document.return_value = mock_interaction
        
        # Mock AI service
        lead_nurturing_service.ai_service.generate_text.return_value = "Generated follow-up message"
        
        # Mock email service
        lead_nurturing_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await lead_nurturing_service.process_follow_up('lead-123', 1, 'workflow-run-123')
        
        # Assertions
        assert result['success'] is True
        assert 'interaction_id' in result
        mock_get_document.assert_any_call('leads', 'lead-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_get_document.assert_any_call('workflow_runs', 'workflow-run-123')
        mock_get_document.assert_any_call('workflow_configs', 'workflow-123')
        mock_query_collection.assert_called_once()
        mock_create_document.assert_called_once()
        mock_update_document.assert_called()
        lead_nurturing_service.email_service.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_process_lead_reply_success(lead_nurturing_service):
    """Test processing a lead reply successfully."""
    # Create a mock inbound interaction
    mock_inbound_interaction = {
        'id': 'interaction-456',
        'company_id': 'company-123',
        'lead_id': 'lead-123',
        'type': 'email',
        'direction': 'inbound',
        'content': 'Thanks for reaching out. I am interested in your services.',
        'channel': 'email',
        'status': 'received',
        'created_at': datetime.now(),
        'metadata': {
            'workflow_run_id': 'workflow-run-123'
        }
    }
    
    # Mock database queries
    with patch('core.database.db.get_document') as mock_get_document, \
         patch('core.database.db.query_collection') as mock_query_collection, \
         patch('core.database.db.create_document') as mock_create_document, \
         patch('core.database.db.update_document') as mock_update_document:
        
        # Set up mock returns
        mock_get_document.side_effect = lambda collection, doc_id: {
            ('interactions', 'interaction-456'): mock_inbound_interaction,
            ('leads', 'lead-123'): mock_lead,
            ('companies', 'company-123'): mock_company,
            ('workflow_runs', 'workflow-run-123'): mock_workflow_run,
            ('workflow_configs', 'workflow-123'): mock_workflow_config
        }.get((collection, doc_id))
        
        mock_query_collection.return_value = [mock_interaction]
        mock_create_document.return_value = {
            'id': 'interaction-789',
            'company_id': 'company-123',
            'lead_id': 'lead-123',
            'type': 'email',
            'direction': 'outbound',
            'content': 'Generated reply response',
            'channel': 'automated_workflow',
            'status': 'delivered',
            'created_at': datetime.now(),
            'metadata': {
                'subject': 'Re: Thanks for your interest in Acme Inc.',
                'workflow_run_id': 'workflow-run-123',
                'in_response_to': 'interaction-456'
            }
        }
        
        # Mock AI service
        lead_nurturing_service.ai_service.generate_text.return_value = "Generated reply response"
        
        # Mock email service
        lead_nurturing_service.email_service.send_email.return_value = {'success': True}
        
        # Call the method
        result = await lead_nurturing_service.process_lead_reply('interaction-456')
        
        # Assertions
        assert result['success'] is True
        assert 'interaction_id' in result
        mock_get_document.assert_any_call('interactions', 'interaction-456')
        mock_get_document.assert_any_call('leads', 'lead-123')
        mock_get_document.assert_any_call('companies', 'company-123')
        mock_get_document.assert_any_call('workflow_runs', 'workflow-run-123')
        mock_get_document.assert_any_call('workflow_configs', 'workflow-123')
        mock_query_collection.assert_called_once()
        mock_create_document.assert_called_once()
        mock_update_document.assert_called()
        lead_nurturing_service.email_service.send_email.assert_called_once()

