"""
API router for lead management and nurturing.

This module provides the API endpoints for managing leads and interactions.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from models.lead import Lead, LeadCreate, LeadUpdate, LeadFilter, Interaction, InteractionCreate
from services.lead_service import LeadService
from services.scheduler.scheduler_service import SchedulerService
from core.security import get_current_user, get_current_company

router = APIRouter()
lead_service = LeadService()
scheduler_service = SchedulerService()


@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Create a new lead.
    
    This endpoint creates a new lead in the system.
    """
    # Set company ID from authenticated user
    lead_in.company_id = current_company["id"]
    
    # Create lead
    lead = lead_service.create_lead(lead_in)
    
    # Schedule follow-up if auto_followup is enabled
    if lead_in.auto_followup:
        scheduler_service.schedule_lead_followup(lead.id, lead.company_id, 24)  # First follow-up after 24 hours
        scheduler_service.schedule_lead_followup(lead.id, lead.company_id, 72)  # Second follow-up after 72 hours
    
    return lead


@router.get("/", response_model=List[Lead])
async def get_leads(
    status: Optional[str] = Query(None, description="Filter by lead status"),
    source: Optional[str] = Query(None, description="Filter by lead source"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned user"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date (after)"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date (before)"),
    skip: int = Query(0, ge=0, description="Number of leads to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of leads to return"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get leads with optional filtering.
    
    This endpoint retrieves leads with optional filtering criteria.
    """
    # Create filter
    lead_filter = LeadFilter(
        status=status,
        source=source,
        assigned_to=assigned_to,
        tags=tags,
        created_after=created_after,
        created_before=created_before
    )
    
    # Get leads
    leads = lead_service.get_leads(current_company["id"], lead_filter, skip, limit)
    
    return leads


@router.get("/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: str = Path(..., description="ID of the lead"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get a lead by ID.
    
    This endpoint retrieves a specific lead by ID.
    """
    lead = lead_service.get_lead(current_company["id"], lead_id)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with ID {lead_id} not found"
        )
    
    return lead


@router.put("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: str = Path(..., description="ID of the lead"),
    lead_update: LeadUpdate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Update a lead.
    
    This endpoint updates a specific lead by ID.
    """
    lead = lead_service.update_lead(current_company["id"], lead_id, lead_update)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with ID {lead_id} not found"
        )
    
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: str = Path(..., description="ID of the lead"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Delete a lead.
    
    This endpoint deletes a specific lead by ID.
    """
    success = lead_service.delete_lead(current_company["id"], lead_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with ID {lead_id} not found"
        )
    
    return None


@router.get("/{lead_id}/interactions", response_model=List[Interaction])
async def get_lead_interactions(
    lead_id: str = Path(..., description="ID of the lead"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get interactions for a lead.
    
    This endpoint retrieves all interactions for a specific lead.
    """
    interactions = lead_service.get_lead_interactions(current_company["id"], lead_id)
    
    return interactions


@router.post("/{lead_id}/interactions", response_model=Interaction, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    lead_id: str = Path(..., description="ID of the lead"),
    interaction_in: InteractionCreate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Create a new interaction for a lead.
    
    This endpoint creates a new interaction for a specific lead.
    """
    # Set company ID and lead ID
    interaction_in.company_id = current_company["id"]
    interaction_in.lead_id = lead_id
    
    # Set created_by if not provided
    if not interaction_in.created_by:
        interaction_in.created_by = current_user["id"]
    
    # Create interaction
    interaction = lead_service.create_interaction(interaction_in)
    
    return interaction


@router.post("/{lead_id}/message", response_model=Dict[str, Any])
async def generate_and_send_message(
    lead_id: str = Path(..., description="ID of the lead"),
    message_type: str = Query("initial_contact", description="Type of message to generate"),
    channel: str = Query("email", description="Channel to use for sending (email or sms)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Generate and send a message to a lead.
    
    This endpoint generates a personalized message for a lead and sends it via the specified channel.
    """
    # Generate message
    message = lead_service.generate_lead_message(lead_id, current_company["id"], message_type)
    
    # Send message
    success = lead_service.send_lead_message(lead_id, current_company["id"], message, channel)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send message to lead {lead_id} via {channel}"
        )
    
    return {
        "success": True,
        "lead_id": lead_id,
        "message_type": message_type,
        "channel": channel,
        "message": message
    }

