"""
Lead Nurturing API Routes

This module contains the API routes for the Lead Nurturing Agent workflow.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import Dict, Any, List, Optional

from core.security import get_current_user
from workflows.lead_nurturing.service import lead_nurturing_service

router = APIRouter(
    prefix="/api/workflows/lead-nurturing",
    tags=["lead-nurturing"],
    responses={404: {"description": "Not found"}},
)

@router.post("/process-lead/{lead_id}")
async def process_lead(
    lead_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a new lead by sending an initial contact message.
    
    Args:
        lead_id: ID of the lead to process
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(lead_nurturing_service.process_new_lead, lead_id)
    
    return {
        "message": f"Processing lead {lead_id} in the background",
        "status": "pending"
    }

@router.post("/process-follow-up/{lead_id}")
async def process_follow_up(
    lead_id: str,
    follow_up_number: int,
    workflow_run_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a follow-up for a lead.
    
    Args:
        lead_id: ID of the lead to follow up with
        follow_up_number: Number of the follow-up (1 for first follow-up, 2 for second, etc.)
        workflow_run_id: ID of the workflow run
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        lead_nurturing_service.process_follow_up, 
        lead_id, 
        follow_up_number, 
        workflow_run_id
    )
    
    return {
        "message": f"Processing follow-up {follow_up_number} for lead {lead_id} in the background",
        "status": "pending"
    }

@router.post("/process-reply/{interaction_id}")
async def process_reply(
    interaction_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a reply from a lead.
    
    Args:
        interaction_id: ID of the interaction containing the lead's reply
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(lead_nurturing_service.process_lead_reply, interaction_id)
    
    return {
        "message": f"Processing reply {interaction_id} in the background",
        "status": "pending"
    }

@router.post("/webhook/email-reply")
async def webhook_email_reply(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for receiving email replies from leads.
    
    Args:
        payload: Webhook payload containing email data
        background_tasks: FastAPI background tasks
        
    Returns:
        Result of the operation
    """
    try:
        # Extract email data from payload
        from_email = payload.get("from", {}).get("email")
        subject = payload.get("subject", "")
        body = payload.get("text", "")
        
        if not from_email or not body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields in webhook payload"
            )
        
        # TODO: Implement logic to find the lead by email and create an interaction
        
        return {
            "message": "Email reply received and will be processed",
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )

@router.post("/webhook/sms-reply")
async def webhook_sms_reply(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for receiving SMS replies from leads.
    
    Args:
        payload: Webhook payload containing SMS data
        background_tasks: FastAPI background tasks
        
    Returns:
        Result of the operation
    """
    try:
        # Extract SMS data from payload
        from_phone = payload.get("from")
        body = payload.get("body", "")
        
        if not from_phone or not body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields in webhook payload"
            )
        
        # TODO: Implement logic to find the lead by phone and create an interaction
        
        return {
            "message": "SMS reply received and will be processed",
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )

