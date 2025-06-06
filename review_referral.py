"""
Review & Referral API Routes

This module contains the API routes for the Review & Referral Generator workflow.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from core.security import get_current_user
from workflows.review_referral.service import review_referral_service

router = APIRouter(
    prefix="/api/workflows/review-referral",
    tags=["review-referral"],
    responses={404: {"description": "Not found"}},
)

class ReviewSubmission(BaseModel):
    """Review submission model."""
    rating: int
    content: str
    platform: str

@router.post("/process-sale/{sale_id}")
async def process_sale(
    sale_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a completed sale by sending a review request.
    
    Args:
        sale_id: ID of the completed sale
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(review_referral_service.process_completed_sale, sale_id)
    
    return {
        "message": f"Processing sale {sale_id} in the background",
        "status": "pending"
    }

@router.post("/send-review-request/{review_id}")
async def send_review_request(
    review_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Send a review request to a customer.
    
    Args:
        review_id: ID of the review record
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(review_referral_service.send_review_request, review_id)
    
    return {
        "message": f"Sending review request {review_id} in the background",
        "status": "pending"
    }

@router.post("/process-review/{review_id}")
async def process_review(
    review_id: str,
    review_submission: ReviewSubmission,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a submitted review and generate a referral offer.
    
    Args:
        review_id: ID of the review record
        review_submission: Review submission data
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        review_referral_service.process_submitted_review,
        review_id,
        review_submission.rating,
        review_submission.content,
        review_submission.platform
    )
    
    return {
        "message": f"Processing review {review_id} in the background",
        "status": "pending"
    }

@router.post("/send-referral-reminder/{referral_id}")
async def send_referral_reminder(
    referral_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Send a reminder about an unused referral code.
    
    Args:
        referral_id: ID of the referral record
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(review_referral_service.send_referral_reminder, referral_id)
    
    return {
        "message": f"Sending referral reminder {referral_id} in the background",
        "status": "pending"
    }

@router.post("/process-referral-use")
async def process_referral_use(
    referral_code: str,
    lead_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process the use of a referral code by a new lead.
    
    Args:
        referral_code: Referral code used
        lead_id: ID of the new lead
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        review_referral_service.process_referral_use,
        referral_code,
        lead_id
    )
    
    return {
        "message": f"Processing referral code {referral_code} use in the background",
        "status": "pending"
    }

@router.post("/webhook/review-submission")
async def webhook_review_submission(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for receiving review submissions from external platforms.
    
    Args:
        payload: Webhook payload containing review data
        background_tasks: FastAPI background tasks
        
    Returns:
        Result of the operation
    """
    try:
        # Extract review data from payload
        customer_email = payload.get("customer_email")
        review_platform = payload.get("platform")
        rating = payload.get("rating")
        content = payload.get("content", "")
        
        if not customer_email or not review_platform or not rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields in webhook payload"
            )
        
        # TODO: Implement logic to find the review by customer email and update it
        
        return {
            "message": "Review submission received and will be processed",
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing webhook: {str(e)}"
        )

