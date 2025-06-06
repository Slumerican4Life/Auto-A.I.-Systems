"""
Lead Service for Business Automation System.

This module provides the service layer for lead management and nurturing.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from models.lead import Lead, LeadCreate, LeadUpdate, LeadFilter, Interaction, InteractionCreate
from services.ai.ai_service import AIService
from services.email.email_service import EmailService
from services.sms.sms_service import SMSService
from services.analytics.analytics_service import AnalyticsService


class LeadService:
    """Service for lead management and nurturing."""

    def __init__(self):
        """Initialize the lead service."""
        self.ai_service = AIService()
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.analytics_service = AnalyticsService()

    def create_lead(self, lead_in: LeadCreate) -> Lead:
        """
        Create a new lead.
        
        Args:
            lead_in: Lead creation data
            
        Returns:
            Created lead
        """
        # Generate ID if not provided
        if not lead_in.id:
            lead_in.id = str(uuid.uuid4())
        
        # Set created_at if not provided
        if not lead_in.created_at:
            lead_in.created_at = datetime.utcnow()
        
        # Set status to "new" if not provided
        if not lead_in.status:
            lead_in.status = "new"
        
        # In a real implementation, this would save to the database
        # For now, we'll just return a mock lead
        lead = Lead(
            id=lead_in.id,
            company_id=lead_in.company_id,
            name=lead_in.name,
            email=lead_in.email,
            phone=lead_in.phone,
            source=lead_in.source,
            status=lead_in.status,
            assigned_to=lead_in.assigned_to,
            tags=lead_in.tags or [],
            metadata=lead_in.metadata or {},
            created_at=lead_in.created_at,
            updated_at=lead_in.created_at
        )
        
        return lead

    def get_leads(self, company_id: str, lead_filter: LeadFilter, skip: int = 0, limit: int = 100) -> List[Lead]:
        """
        Get leads with optional filtering.
        
        Args:
            company_id: ID of the company
            lead_filter: Filter criteria
            skip: Number of leads to skip
            limit: Maximum number of leads to return
            
        Returns:
            List of leads
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock list of leads
        leads = [
            Lead(
                id=str(uuid.uuid4()),
                company_id=company_id,
                name="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                source="website",
                status="new",
                assigned_to=None,
                tags=["website", "contact-form"],
                metadata={},
                created_at=datetime.utcnow() - timedelta(days=1),
                updated_at=datetime.utcnow() - timedelta(days=1)
            ),
            Lead(
                id=str(uuid.uuid4()),
                company_id=company_id,
                name="Jane Smith",
                email="jane.smith@example.com",
                phone="+1987654321",
                source="facebook-ad",
                status="contacted",
                assigned_to="user123",
                tags=["facebook", "ad-campaign-1"],
                metadata={},
                created_at=datetime.utcnow() - timedelta(days=3),
                updated_at=datetime.utcnow() - timedelta(days=2)
            )
        ]
        
        # Apply filters
        filtered_leads = leads
        if lead_filter.status:
            filtered_leads = [lead for lead in filtered_leads if lead.status == lead_filter.status]
        if lead_filter.source:
            filtered_leads = [lead for lead in filtered_leads if lead.source == lead_filter.source]
        if lead_filter.assigned_to:
            filtered_leads = [lead for lead in filtered_leads if lead.assigned_to == lead_filter.assigned_to]
        if lead_filter.tags:
            filtered_leads = [lead for lead in filtered_leads if any(tag in lead.tags for tag in lead_filter.tags)]
        if lead_filter.created_after:
            filtered_leads = [lead for lead in filtered_leads if lead.created_at >= lead_filter.created_after]
        if lead_filter.created_before:
            filtered_leads = [lead for lead in filtered_leads if lead.created_at <= lead_filter.created_before]
        
        # Apply pagination
        paginated_leads = filtered_leads[skip:skip + limit]
        
        return paginated_leads

    def get_lead(self, company_id: str, lead_id: str) -> Optional[Lead]:
        """
        Get a lead by ID.
        
        Args:
            company_id: ID of the company
            lead_id: ID of the lead
            
        Returns:
            Lead or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock lead
        if lead_id == "mock_lead_id":
            return Lead(
                id=lead_id,
                company_id=company_id,
                name="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                source="website",
                status="new",
                assigned_to=None,
                tags=["website", "contact-form"],
                metadata={},
                created_at=datetime.utcnow() - timedelta(days=1),
                updated_at=datetime.utcnow() - timedelta(days=1)
            )
        
        return None

    def update_lead(self, company_id: str, lead_id: str, lead_update: LeadUpdate) -> Lead:
        """
        Update a lead.
        
        Args:
            company_id: ID of the company
            lead_id: ID of the lead
            lead_update: Lead update data
            
        Returns:
            Updated lead
        """
        # In a real implementation, this would update the database
        # For now, we'll just return a mock updated lead
        lead = self.get_lead(company_id, lead_id)
        
        if not lead:
            # In a real implementation, this would raise an exception
            # For now, we'll just return a mock lead
            lead = Lead(
                id=lead_id,
                company_id=company_id,
                name="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                source="website",
                status="new",
                assigned_to=None,
                tags=["website", "contact-form"],
                metadata={},
                created_at=datetime.utcnow() - timedelta(days=1),
                updated_at=datetime.utcnow() - timedelta(days=1)
            )
        
        # Update fields
        if lead_update.name:
            lead.name = lead_update.name
        if lead_update.email:
            lead.email = lead_update.email
        if lead_update.phone:
            lead.phone = lead_update.phone
        if lead_update.status:
            lead.status = lead_update.status
        if lead_update.assigned_to:
            lead.assigned_to = lead_update.assigned_to
        if lead_update.tags:
            lead.tags = lead_update.tags
        if lead_update.metadata:
            lead.metadata = {**lead.metadata, **lead_update.metadata}
        
        lead.updated_at = datetime.utcnow()
        
        return lead

    def delete_lead(self, company_id: str, lead_id: str) -> bool:
        """
        Delete a lead.
        
        Args:
            company_id: ID of the company
            lead_id: ID of the lead
            
        Returns:
            True if deleted, False otherwise
        """
        # In a real implementation, this would delete from the database
        # For now, we'll just return True
        return True

    def get_lead_interactions(self, company_id: str, lead_id: str) -> List[Interaction]:
        """
        Get interactions for a lead.
        
        Args:
            company_id: ID of the company
            lead_id: ID of the lead
            
        Returns:
            List of interactions
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock list of interactions
        interactions = [
            Interaction(
                id=str(uuid.uuid4()),
                company_id=company_id,
                lead_id=lead_id,
                type="email",
                direction="outbound",
                content="Hello, thank you for your interest in our services. How can we help you?",
                channel="automated",
                created_by="system",
                created_at=datetime.utcnow() - timedelta(days=1),
                metadata={"subject": "Thank you for your interest"}
            ),
            Interaction(
                id=str(uuid.uuid4()),
                company_id=company_id,
                lead_id=lead_id,
                type="email",
                direction="inbound",
                content="Hi, I'm interested in learning more about your pricing.",
                channel="email",
                created_by=None,
                created_at=datetime.utcnow() - timedelta(hours=12),
                metadata={"subject": "Re: Thank you for your interest"}
            )
        ]
        
        return interactions

    def create_interaction(self, interaction_in: InteractionCreate) -> Interaction:
        """
        Create a new interaction for a lead.
        
        Args:
            interaction_in: Interaction creation data
            
        Returns:
            Created interaction
        """
        # Generate ID if not provided
        if not interaction_in.id:
            interaction_in.id = str(uuid.uuid4())
        
        # Set created_at if not provided
        if not interaction_in.created_at:
            interaction_in.created_at = datetime.utcnow()
        
        # In a real implementation, this would save to the database
        # For now, we'll just return a mock interaction
        interaction = Interaction(
            id=interaction_in.id,
            company_id=interaction_in.company_id,
            lead_id=interaction_in.lead_id,
            type=interaction_in.type,
            direction=interaction_in.direction,
            content=interaction_in.content,
            channel=interaction_in.channel,
            created_by=interaction_in.created_by,
            created_at=interaction_in.created_at,
            metadata=interaction_in.metadata or {}
        )
        
        return interaction

    def generate_lead_message(self, lead_id: str, company_id: str, message_type: str) -> str:
        """
        Generate a message for a lead using AI.
        
        Args:
            lead_id: ID of the lead
            company_id: ID of the company
            message_type: Type of message to generate
            
        Returns:
            Generated message
        """
        # Get lead
        lead = self.get_lead(company_id, lead_id)
        
        if not lead:
            return "Error: Lead not found"
        
        # Generate message using AI
        message_params = {
            "lead_name": lead.name,
            "company_id": company_id,
            "lead_source": lead.source,
            "message_type": message_type
        }
        
        return self.ai_service.generate_lead_message(message_params)

    def send_lead_message(self, lead_id: str, company_id: str, message: str, channel: str) -> bool:
        """
        Send a message to a lead.
        
        Args:
            lead_id: ID of the lead
            company_id: ID of the company
            message: Message content
            channel: Channel to use (email or sms)
            
        Returns:
            True if sent, False otherwise
        """
        # Get lead
        lead = self.get_lead(company_id, lead_id)
        
        if not lead:
            return False
        
        # Send message
        if channel == "email" and lead.email:
            # Send email
            self.email_service.send_email(
                to_email=lead.email,
                subject=f"Following up on your interest",
                content=message,
                company_id=company_id
            )
            
            # Create interaction
            interaction_in = InteractionCreate(
                company_id=company_id,
                lead_id=lead_id,
                type="email",
                direction="outbound",
                content=message,
                channel="automated",
                created_by="system",
                metadata={"subject": "Following up on your interest"}
            )
            
            self.create_interaction(interaction_in)
            
            return True
        elif channel == "sms" and lead.phone:
            # Send SMS
            self.sms_service.send_sms(
                to_phone=lead.phone,
                content=message,
                company_id=company_id
            )
            
            # Create interaction
            interaction_in = InteractionCreate(
                company_id=company_id,
                lead_id=lead_id,
                type="sms",
                direction="outbound",
                content=message,
                channel="automated",
                created_by="system",
                metadata={}
            )
            
            self.create_interaction(interaction_in)
            
            return True
        
        return False

