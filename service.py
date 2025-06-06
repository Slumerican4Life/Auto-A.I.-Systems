"""
Lead Nurturing Agent Service

This module contains the service layer for the Lead Nurturing Agent workflow.
It handles the business logic for nurturing leads through automated follow-ups.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

from core.database import db
from services.ai.openai_service import OpenAIService
from services.email.email_service import EmailService
from services.sms.sms_service import SmsService
from workflows.lead_nurturing.prompts import (
    INITIAL_CONTACT_PROMPT,
    FOLLOW_UP_PROMPT,
    FINAL_FOLLOW_UP_PROMPT,
    LEAD_REPLY_PROMPT,
    SUBJECT_LINE_PROMPT
)

logger = logging.getLogger(__name__)

class LeadNurturingService:
    """Service for handling lead nurturing workflows."""
    
    def __init__(self):
        """Initialize the service with required dependencies."""
        self.ai_service = OpenAIService()
        self.email_service = EmailService()
        self.sms_service = SmsService()
    
    async def process_new_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Process a new lead by sending an initial contact message.
        
        Args:
            lead_id: ID of the lead to process
            
        Returns:
            Result of the operation
        """
        try:
            # Get lead data
            lead = await db.get_document('leads', lead_id)
            if not lead:
                raise ValueError(f"Lead not found: {lead_id}")
            
            # Get company data
            company = await db.get_document('companies', lead['company_id'])
            if not company:
                raise ValueError(f"Company not found: {lead['company_id']}")
            
            # Get workflow config
            workflow_configs = await db.query_collection(
                'workflow_configs',
                filters=[
                    {'field': 'company_id', 'op': '==', 'value': lead['company_id']},
                    {'field': 'workflow_type', 'op': '==', 'value': 'lead_nurturing'},
                    {'field': 'active', 'op': '==', 'value': True}
                ]
            )
            
            if not workflow_configs:
                logger.warning(f"No active lead nurturing workflow found for company {lead['company_id']}")
                return {'success': False, 'message': 'No active workflow found'}
            
            # Use the first active workflow config
            workflow_config = workflow_configs[0]
            
            # Check if lead source matches workflow triggers
            lead_source = lead.get('source', '')
            if 'triggers' in workflow_config and 'lead_source' in workflow_config['triggers']:
                if lead_source not in workflow_config['triggers']['lead_source']:
                    logger.info(f"Lead source '{lead_source}' does not match workflow triggers")
                    return {'success': False, 'message': 'Lead source does not match workflow triggers'}
            
            # Create workflow run
            workflow_run = await db.create_document('workflow_runs', {
                'company_id': lead['company_id'],
                'workflow_config_id': workflow_config['id'],
                'status': 'running',
                'started_at': datetime.now(),
                'trigger_type': 'new_lead',
                'trigger_id': lead_id,
                'actions_performed': [],
                'results': {}
            })
            
            # Generate initial contact message
            message, subject = await self._generate_initial_contact(lead, company, workflow_config)
            
            # Determine channel (email or SMS)
            channel = workflow_config.get('actions', {}).get('channel', 'email')
            
            # Send message
            if channel == 'email':
                # Send email
                email_result = await self.email_service.send_email(
                    to_email=lead['email'],
                    to_name=lead['name'],
                    subject=subject,
                    body=message,
                    from_name=company['name']
                )
                
                # Record interaction
                interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'email',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if email_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'subject': subject,
                        'workflow_run_id': workflow_run['id']
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_email',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['email'],
                        'subject': subject,
                        'status': 'delivered' if email_result['success'] else 'failed',
                        'interaction_id': interaction['id']
                    }
                })
                
                # Schedule follow-ups
                follow_ups = workflow_config.get('actions', {}).get('follow_up', [])
                for i, follow_up in enumerate(follow_ups):
                    delay_hours = follow_up.get('delay_hours', 24)
                    scheduled_time = datetime.now() + timedelta(hours=delay_hours)
                    
                    # Add follow-up to actions performed
                    actions_performed.append({
                        'type': 'schedule_follow_up',
                        'timestamp': datetime.now().isoformat(),
                        'details': {
                            'scheduled_for': scheduled_time.isoformat(),
                            'template': follow_up.get('message_template'),
                            'follow_up_number': i + 1
                        }
                    })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run['id'], {
                    'actions_performed': actions_performed,
                    'results': {
                        'message_sent': email_result['success'],
                        'follow_ups_scheduled': len(follow_ups)
                    }
                })
                
                # Update lead status
                await db.update_document('leads', lead_id, {
                    'status': 'contacted',
                    'updated_at': datetime.now()
                })
                
                return {
                    'success': True,
                    'message': 'Initial contact email sent',
                    'interaction_id': interaction['id'],
                    'workflow_run_id': workflow_run['id']
                }
            
            elif channel == 'sms':
                # Send SMS
                sms_result = await self.sms_service.send_sms(
                    to_phone=lead['phone'],
                    message=message
                )
                
                # Record interaction
                interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'sms',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if sms_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'workflow_run_id': workflow_run['id']
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_sms',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['phone'],
                        'status': 'delivered' if sms_result['success'] else 'failed',
                        'interaction_id': interaction['id']
                    }
                })
                
                # Schedule follow-ups
                follow_ups = workflow_config.get('actions', {}).get('follow_up', [])
                for i, follow_up in enumerate(follow_ups):
                    delay_hours = follow_up.get('delay_hours', 24)
                    scheduled_time = datetime.now() + timedelta(hours=delay_hours)
                    
                    # Add follow-up to actions performed
                    actions_performed.append({
                        'type': 'schedule_follow_up',
                        'timestamp': datetime.now().isoformat(),
                        'details': {
                            'scheduled_for': scheduled_time.isoformat(),
                            'template': follow_up.get('message_template'),
                            'follow_up_number': i + 1
                        }
                    })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run['id'], {
                    'actions_performed': actions_performed,
                    'results': {
                        'message_sent': sms_result['success'],
                        'follow_ups_scheduled': len(follow_ups)
                    }
                })
                
                # Update lead status
                await db.update_document('leads', lead_id, {
                    'status': 'contacted',
                    'updated_at': datetime.now()
                })
                
                return {
                    'success': True,
                    'message': 'Initial contact SMS sent',
                    'interaction_id': interaction['id'],
                    'workflow_run_id': workflow_run['id']
                }
            
            else:
                logger.error(f"Unsupported channel: {channel}")
                return {'success': False, 'message': f'Unsupported channel: {channel}'}
        
        except Exception as e:
            logger.error(f"Error processing new lead {lead_id}: {e}")
            return {'success': False, 'message': str(e)}
    
    async def process_follow_up(self, lead_id: str, follow_up_number: int, workflow_run_id: str) -> Dict[str, Any]:
        """
        Process a follow-up for a lead.
        
        Args:
            lead_id: ID of the lead to follow up with
            follow_up_number: Number of the follow-up (1 for first follow-up, 2 for second, etc.)
            workflow_run_id: ID of the workflow run
            
        Returns:
            Result of the operation
        """
        try:
            # Get lead data
            lead = await db.get_document('leads', lead_id)
            if not lead:
                raise ValueError(f"Lead not found: {lead_id}")
            
            # Get company data
            company = await db.get_document('companies', lead['company_id'])
            if not company:
                raise ValueError(f"Company not found: {lead['company_id']}")
            
            # Get workflow run
            workflow_run = await db.get_document('workflow_runs', workflow_run_id)
            if not workflow_run:
                raise ValueError(f"Workflow run not found: {workflow_run_id}")
            
            # Get workflow config
            workflow_config = await db.get_document('workflow_configs', workflow_run['workflow_config_id'])
            if not workflow_config:
                raise ValueError(f"Workflow config not found: {workflow_run['workflow_config_id']}")
            
            # Check if lead has replied
            interactions = await db.query_collection(
                'interactions',
                filters=[
                    {'field': 'lead_id', 'op': '==', 'value': lead_id},
                    {'field': 'direction', 'op': '==', 'value': 'inbound'},
                    {'field': 'created_at', 'op': '>', 'value': workflow_run['started_at']}
                ]
            )
            
            if interactions:
                logger.info(f"Lead {lead_id} has already replied, skipping follow-up")
                return {'success': True, 'message': 'Lead has already replied, follow-up skipped'}
            
            # Get previous communications
            previous_interactions = await db.query_collection(
                'interactions',
                filters=[
                    {'field': 'lead_id', 'op': '==', 'value': lead_id},
                    {'field': 'direction', 'op': '==', 'value': 'outbound'}
                ],
                order_by='created_at'
            )
            
            # Generate follow-up message
            is_final = follow_up_number >= len(workflow_config.get('actions', {}).get('follow_up', []))
            message, subject = await self._generate_follow_up(
                lead, 
                company, 
                workflow_config, 
                previous_interactions, 
                is_final
            )
            
            # Determine channel (email or SMS)
            channel = workflow_config.get('actions', {}).get('channel', 'email')
            
            # Send message
            if channel == 'email':
                # Send email
                email_result = await self.email_service.send_email(
                    to_email=lead['email'],
                    to_name=lead['name'],
                    subject=subject,
                    body=message,
                    from_name=company['name']
                )
                
                # Record interaction
                interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'email',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if email_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'subject': subject,
                        'workflow_run_id': workflow_run_id,
                        'follow_up_number': follow_up_number
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_follow_up_email',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['email'],
                        'subject': subject,
                        'status': 'delivered' if email_result['success'] else 'failed',
                        'interaction_id': interaction['id'],
                        'follow_up_number': follow_up_number
                    }
                })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run_id, {
                    'actions_performed': actions_performed,
                    'results': {
                        'follow_up_sent': email_result['success'],
                        'follow_up_number': follow_up_number
                    }
                })
                
                return {
                    'success': True,
                    'message': f'Follow-up {follow_up_number} email sent',
                    'interaction_id': interaction['id']
                }
            
            elif channel == 'sms':
                # Send SMS
                sms_result = await self.sms_service.send_sms(
                    to_phone=lead['phone'],
                    message=message
                )
                
                # Record interaction
                interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'sms',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if sms_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'workflow_run_id': workflow_run_id,
                        'follow_up_number': follow_up_number
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_follow_up_sms',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['phone'],
                        'status': 'delivered' if sms_result['success'] else 'failed',
                        'interaction_id': interaction['id'],
                        'follow_up_number': follow_up_number
                    }
                })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run_id, {
                    'actions_performed': actions_performed,
                    'results': {
                        'follow_up_sent': sms_result['success'],
                        'follow_up_number': follow_up_number
                    }
                })
                
                return {
                    'success': True,
                    'message': f'Follow-up {follow_up_number} SMS sent',
                    'interaction_id': interaction['id']
                }
            
            else:
                logger.error(f"Unsupported channel: {channel}")
                return {'success': False, 'message': f'Unsupported channel: {channel}'}
        
        except Exception as e:
            logger.error(f"Error processing follow-up for lead {lead_id}: {e}")
            return {'success': False, 'message': str(e)}
    
    async def process_lead_reply(self, interaction_id: str) -> Dict[str, Any]:
        """
        Process a reply from a lead.
        
        Args:
            interaction_id: ID of the interaction containing the lead's reply
            
        Returns:
            Result of the operation
        """
        try:
            # Get interaction data
            interaction = await db.get_document('interactions', interaction_id)
            if not interaction:
                raise ValueError(f"Interaction not found: {interaction_id}")
            
            # Verify this is an inbound interaction
            if interaction.get('direction') != 'inbound':
                raise ValueError(f"Interaction {interaction_id} is not an inbound interaction")
            
            # Get lead data
            lead_id = interaction.get('lead_id')
            lead = await db.get_document('leads', lead_id)
            if not lead:
                raise ValueError(f"Lead not found: {lead_id}")
            
            # Get company data
            company = await db.get_document('companies', lead['company_id'])
            if not company:
                raise ValueError(f"Company not found: {lead['company_id']}")
            
            # Get workflow run from metadata
            workflow_run_id = interaction.get('metadata', {}).get('workflow_run_id')
            if not workflow_run_id:
                # Find the most recent workflow run for this lead
                workflow_runs = await db.query_collection(
                    'workflow_runs',
                    filters=[
                        {'field': 'trigger_type', 'op': '==', 'value': 'new_lead'},
                        {'field': 'trigger_id', 'op': '==', 'value': lead_id}
                    ],
                    order_by='started_at',
                    order_direction='desc',
                    limit=1
                )
                
                if workflow_runs:
                    workflow_run_id = workflow_runs[0]['id']
                else:
                    logger.warning(f"No workflow run found for lead {lead_id}")
                    return {'success': False, 'message': 'No workflow run found'}
            
            # Get workflow run
            workflow_run = await db.get_document('workflow_runs', workflow_run_id)
            if not workflow_run:
                raise ValueError(f"Workflow run not found: {workflow_run_id}")
            
            # Get workflow config
            workflow_config = await db.get_document('workflow_configs', workflow_run['workflow_config_id'])
            if not workflow_config:
                raise ValueError(f"Workflow config not found: {workflow_run['workflow_config_id']}")
            
            # Get previous communications
            previous_interactions = await db.query_collection(
                'interactions',
                filters=[
                    {'field': 'lead_id', 'op': '==', 'value': lead_id}
                ],
                order_by='created_at'
            )
            
            # Generate response message
            message, subject = await self._generate_reply_response(
                lead,
                company,
                workflow_config,
                previous_interactions,
                interaction
            )
            
            # Determine channel (email or SMS)
            channel = interaction.get('type', 'email')
            
            # Send message
            if channel == 'email':
                # Send email
                email_result = await self.email_service.send_email(
                    to_email=lead['email'],
                    to_name=lead['name'],
                    subject=subject,
                    body=message,
                    from_name=company['name']
                )
                
                # Record interaction
                response_interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'email',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if email_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'subject': subject,
                        'workflow_run_id': workflow_run_id,
                        'in_response_to': interaction_id
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_reply_email',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['email'],
                        'subject': subject,
                        'status': 'delivered' if email_result['success'] else 'failed',
                        'interaction_id': response_interaction['id'],
                        'in_response_to': interaction_id
                    }
                })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run_id, {
                    'actions_performed': actions_performed,
                    'results': {
                        'reply_sent': email_result['success']
                    }
                })
                
                # Update lead status
                await db.update_document('leads', lead_id, {
                    'status': 'engaged',
                    'updated_at': datetime.now()
                })
                
                return {
                    'success': True,
                    'message': 'Reply email sent',
                    'interaction_id': response_interaction['id']
                }
            
            elif channel == 'sms':
                # Send SMS
                sms_result = await self.sms_service.send_sms(
                    to_phone=lead['phone'],
                    message=message
                )
                
                # Record interaction
                response_interaction = await db.create_document('interactions', {
                    'company_id': lead['company_id'],
                    'lead_id': lead_id,
                    'type': 'sms',
                    'direction': 'outbound',
                    'content': message,
                    'channel': 'automated_workflow',
                    'status': 'delivered' if sms_result['success'] else 'failed',
                    'created_at': datetime.now(),
                    'metadata': {
                        'workflow_run_id': workflow_run_id,
                        'in_response_to': interaction_id
                    }
                })
                
                # Update workflow run
                actions_performed = workflow_run.get('actions_performed', [])
                actions_performed.append({
                    'type': 'send_reply_sms',
                    'timestamp': datetime.now().isoformat(),
                    'details': {
                        'to': lead['phone'],
                        'status': 'delivered' if sms_result['success'] else 'failed',
                        'interaction_id': response_interaction['id'],
                        'in_response_to': interaction_id
                    }
                })
                
                # Update workflow run
                await db.update_document('workflow_runs', workflow_run_id, {
                    'actions_performed': actions_performed,
                    'results': {
                        'reply_sent': sms_result['success']
                    }
                })
                
                # Update lead status
                await db.update_document('leads', lead_id, {
                    'status': 'engaged',
                    'updated_at': datetime.now()
                })
                
                return {
                    'success': True,
                    'message': 'Reply SMS sent',
                    'interaction_id': response_interaction['id']
                }
            
            else:
                logger.error(f"Unsupported channel: {channel}")
                return {'success': False, 'message': f'Unsupported channel: {channel}'}
        
        except Exception as e:
            logger.error(f"Error processing lead reply {interaction_id}: {e}")
            return {'success': False, 'message': str(e)}
    
    async def _generate_initial_contact(
        self, 
        lead: Dict[str, Any], 
        company: Dict[str, Any], 
        workflow_config: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Generate an initial contact message for a lead.
        
        Args:
            lead: Lead data
            company: Company data
            workflow_config: Workflow configuration
            
        Returns:
            Tuple of (message, subject)
        """
        # Prepare prompt variables
        prompt_vars = {
            'business_name': company.get('name', ''),
            'industry': company.get('industry', ''),
            'products_services': company.get('settings', {}).get('products_services', ''),
            'value_proposition': company.get('settings', {}).get('value_proposition', ''),
            'lead_name': lead.get('name', ''),
            'lead_email': lead.get('email', ''),
            'lead_source': lead.get('source', ''),
            'lead_message': lead.get('notes', ''),
            'additional_context': ''
        }
        
        # Check if there's a custom template in the workflow config
        template_key = workflow_config.get('actions', {}).get('message_template', '')
        custom_template = workflow_config.get('templates', {}).get(template_key, '')
        
        if custom_template:
            # Use custom template with variable substitution
            message = custom_template
            for key, value in prompt_vars.items():
                message = message.replace(f"{{{{{key}}}}}", value)
        else:
            # Use AI to generate message
            prompt = INITIAL_CONTACT_PROMPT.format(**prompt_vars)
            message = await self.ai_service.generate_text(prompt)
        
        # Generate subject line
        subject_vars = {
            'email_type': 'initial contact',
            'lead_name': lead.get('name', ''),
            'business_name': company.get('name', ''),
            'lead_message': lead.get('notes', ''),
            'email_purpose': 'introduce the business and respond to the lead\'s inquiry'
        }
        
        subject_prompt = SUBJECT_LINE_PROMPT.format(**subject_vars)
        subject = await self.ai_service.generate_text(subject_prompt)
        
        return message, subject
    
    async def _generate_follow_up(
        self, 
        lead: Dict[str, Any], 
        company: Dict[str, Any], 
        workflow_config: Dict[str, Any],
        previous_interactions: List[Dict[str, Any]],
        is_final: bool
    ) -> Tuple[str, str]:
        """
        Generate a follow-up message for a lead.
        
        Args:
            lead: Lead data
            company: Company data
            workflow_config: Workflow configuration
            previous_interactions: Previous interactions with the lead
            is_final: Whether this is the final follow-up
            
        Returns:
            Tuple of (message, subject)
        """
        # Extract previous communications
        previous_communications = []
        for interaction in previous_interactions:
            if interaction.get('direction') == 'outbound':
                previous_communications.append({
                    'timestamp': interaction.get('created_at'),
                    'content': interaction.get('content', ''),
                    'type': interaction.get('type', 'email'),
                    'subject': interaction.get('metadata', {}).get('subject', '')
                })
        
        # Calculate days since first contact
        first_contact = None
        for interaction in previous_interactions:
            if interaction.get('direction') == 'outbound':
                first_contact = interaction.get('created_at')
                break
        
        days_since_contact = 0
        if first_contact:
            days_since_contact = (datetime.now() - first_contact).days
        
        # Prepare prompt variables
        prompt_vars = {
            'business_name': company.get('name', ''),
            'industry': company.get('industry', ''),
            'products_services': company.get('settings', {}).get('products_services', ''),
            'value_proposition': company.get('settings', {}).get('value_proposition', ''),
            'lead_name': lead.get('name', ''),
            'lead_email': lead.get('email', ''),
            'lead_source': lead.get('source', ''),
            'lead_message': lead.get('notes', ''),
            'previous_communications': '\n\n'.join([f"Message {i+1}:\n{comm.get('content', '')}" for i, comm in enumerate(previous_communications)]),
            'days_since_contact': days_since_contact,
            'days_since_first_contact': days_since_contact,
            'additional_context': ''
        }
        
        # Check if there's a custom template in the workflow config
        follow_ups = workflow_config.get('actions', {}).get('follow_up', [])
        template_key = None
        if follow_ups and len(follow_ups) > 0:
            if is_final and len(follow_ups) > 1:
                template_key = follow_ups[-1].get('message_template', '')
            else:
                template_key = follow_ups[0].get('message_template', '')
        
        custom_template = workflow_config.get('templates', {}).get(template_key, '')
        
        if custom_template:
            # Use custom template with variable substitution
            message = custom_template
            for key, value in prompt_vars.items():
                message = message.replace(f"{{{{{key}}}}}", str(value))
        else:
            # Use AI to generate message
            if is_final:
                prompt = FINAL_FOLLOW_UP_PROMPT.format(**prompt_vars)
            else:
                prompt = FOLLOW_UP_PROMPT.format(**prompt_vars)
            
            message = await self.ai_service.generate_text(prompt)
        
        # Generate subject line
        subject_vars = {
            'email_type': 'follow-up',
            'lead_name': lead.get('name', ''),
            'business_name': company.get('name', ''),
            'lead_message': lead.get('notes', ''),
            'email_purpose': 'follow up on the initial inquiry and provide additional value'
        }
        
        subject_prompt = SUBJECT_LINE_PROMPT.format(**subject_vars)
        subject = await self.ai_service.generate_text(subject_prompt)
        
        return message, subject
    
    async def _generate_reply_response(
        self, 
        lead: Dict[str, Any], 
        company: Dict[str, Any], 
        workflow_config: Dict[str, Any],
        previous_interactions: List[Dict[str, Any]],
        lead_reply: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Generate a response to a lead's reply.
        
        Args:
            lead: Lead data
            company: Company data
            workflow_config: Workflow configuration
            previous_interactions: Previous interactions with the lead
            lead_reply: The lead's reply interaction
            
        Returns:
            Tuple of (message, subject)
        """
        # Extract previous communications
        previous_communications = []
        for interaction in previous_interactions:
            if interaction['id'] != lead_reply['id']:  # Exclude the current reply
                previous_communications.append({
                    'timestamp': interaction.get('created_at'),
                    'content': interaction.get('content', ''),
                    'type': interaction.get('type', 'email'),
                    'direction': interaction.get('direction', 'outbound'),
                    'subject': interaction.get('metadata', {}).get('subject', '')
                })
        
        # Prepare prompt variables
        prompt_vars = {
            'business_name': company.get('name', ''),
            'industry': company.get('industry', ''),
            'products_services': company.get('settings', {}).get('products_services', ''),
            'value_proposition': company.get('settings', {}).get('value_proposition', ''),
            'lead_name': lead.get('name', ''),
            'lead_email': lead.get('email', ''),
            'lead_source': lead.get('source', ''),
            'lead_message': lead.get('notes', ''),
            'previous_communications': '\n\n'.join([
                f"{'→' if comm.get('direction') == 'outbound' else '←'} {comm.get('content', '')}"
                for comm in previous_communications
            ]),
            'lead_reply': lead_reply.get('content', ''),
            'additional_context': ''
        }
        
        # Use AI to generate message
        prompt = LEAD_REPLY_PROMPT.format(**prompt_vars)
        message = await self.ai_service.generate_text(prompt)
        
        # Generate subject line
        subject = "Re: "
        
        # Try to find the original subject
        for interaction in previous_interactions:
            if interaction.get('direction') == 'outbound' and interaction.get('type') == 'email':
                original_subject = interaction.get('metadata', {}).get('subject', '')
                if original_subject:
                    # Check if it already has Re: prefix
                    if not original_subject.startswith('Re:'):
                        subject += original_subject
                    else:
                        subject = original_subject
                    break
        
        # If no original subject found, generate one
        if subject == "Re: ":
            subject_vars = {
                'email_type': 'response',
                'lead_name': lead.get('name', ''),
                'business_name': company.get('name', ''),
                'lead_message': lead_reply.get('content', ''),
                'email_purpose': 'respond to the lead\'s specific questions or comments'
            }
            
            subject_prompt = SUBJECT_LINE_PROMPT.format(**subject_vars)
            subject = await self.ai_service.generate_text(subject_prompt)
        
        return message, subject

# Create service instance
lead_nurturing_service = LeadNurturingService()

