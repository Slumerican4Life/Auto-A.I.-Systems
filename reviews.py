"""
API router for review and referral management.

This module provides the API endpoints for managing reviews and referrals.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from models.review_referral import (
    Review, ReviewRequestCreate, ReviewUpdate, ReviewFilter,
    Referral, ReferralCreate, ReferralFilter, Customer
)
from services.review_service import ReviewService
from services.scheduler.scheduler_service import SchedulerService
from core.security import get_current_user, get_current_company

router = APIRouter()
review_service = ReviewService()
scheduler_service = SchedulerService()


@router.post("/request", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review_request(
    review_request: ReviewRequestCreate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Create a new review request.
    
    This endpoint creates a new review request for a customer.
    """
    # Set company ID from authenticated user
    review_request.company_id = current_company["id"]
    
    # Create review request
    review = review_service.create_review_request(review_request)
    
    return review


@router.get("/", response_model=List[Review])
async def get_reviews(
    status: Optional[str] = Query(None, description="Filter by review status"),
    platform: Optional[str] = Query(None, description="Filter by review platform"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter by rating"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date (after)"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date (before)"),
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of reviews to return"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get reviews with optional filtering.
    
    This endpoint retrieves reviews with optional filtering criteria.
    """
    # Create filter
    review_filter = ReviewFilter(
        status=status,
        platform=platform,
        rating=rating,
        created_after=created_after,
        created_before=created_before
    )
    
    # Get reviews
    reviews = review_service.get_reviews(current_company["id"], review_filter, skip, limit)
    
    return reviews


@router.get("/{review_id}", response_model=Review)
async def get_review(
    review_id: str = Path(..., description="ID of the review"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get a review by ID.
    
    This endpoint retrieves a specific review by ID.
    """
    review = review_service.get_review(current_company["id"], review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID {review_id} not found"
        )
    
    return review


@router.put("/{review_id}", response_model=Review)
async def update_review(
    review_id: str = Path(..., description="ID of the review"),
    review_update: ReviewUpdate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Update a review.
    
    This endpoint updates a specific review by ID.
    """
    review = review_service.update_review(current_company["id"], review_id, review_update)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID {review_id} not found"
        )
    
    # If review is completed and has a positive rating (4 or 5), create a referral
    if review_update.status == "completed" and review_update.rating and review_update.rating >= 4:
        # Generate referral code
        referral_code = review_service.generate_referral_code(current_company["id"], review.customer_id)
        
        # Create referral
        referral_create = ReferralCreate(
            company_id=current_company["id"],
            customer_id=review.customer_id,
            offer_details="10% discount for you and your friend",
            max_uses=3
        )
        
        referral = review_service.create_referral(referral_create, referral_code)
        
        # Add referral ID to review metadata
        review_service.update_review(
            current_company["id"],
            review_id,
            ReviewUpdate(metadata={"referral_id": referral.id})
        )
    
    return review


@router.post("/{review_id}/send-referral", response_model=Dict[str, Any])
async def send_referral_offer(
    review_id: str = Path(..., description="ID of the review"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Send a referral offer for a completed review.
    
    This endpoint sends a referral offer to a customer who has completed a review.
    """
    # Get review
    review = review_service.get_review(current_company["id"], review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID {review_id} not found"
        )
    
    # Check if review is completed
    if review.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review must be completed before sending referral offer"
        )
    
    # Check if review has a positive rating
    if not review.rating or review.rating < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review must have a positive rating (4 or 5) to send referral offer"
        )
    
    # Check if referral already exists
    referral_id = review.metadata.get("referral_id")
    if not referral_id:
        # Generate referral code
        referral_code = review_service.generate_referral_code(current_company["id"], review.customer_id)
        
        # Create referral
        referral_create = ReferralCreate(
            company_id=current_company["id"],
            customer_id=review.customer_id,
            offer_details="10% discount for you and your friend",
            max_uses=3
        )
        
        referral = review_service.create_referral(referral_create, referral_code)
        
        # Add referral ID to review metadata
        review_service.update_review(
            current_company["id"],
            review_id,
            ReviewUpdate(metadata={"referral_id": referral.id})
        )
    else:
        # Get existing referral
        referral = review_service.get_referral(current_company["id"], referral_id)
        
        if not referral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Referral with ID {referral_id} not found"
            )
    
    # In a real implementation, this would send the referral offer via email or SMS
    # For now, we'll just return the referral details
    
    return {
        "success": True,
        "review_id": review_id,
        "referral_id": referral.id,
        "referral_code": referral.code,
        "offer_details": referral.offer_details
    }


@router.get("/referrals/", response_model=List[Referral])
async def get_referrals(
    status: Optional[str] = Query(None, description="Filter by referral status (active, expired, used)"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date (after)"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date (before)"),
    skip: int = Query(0, ge=0, description="Number of referrals to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of referrals to return"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get referrals with optional filtering.
    
    This endpoint retrieves referrals with optional filtering criteria.
    """
    # Create filter
    referral_filter = ReferralFilter(
        status=status,
        customer_id=customer_id,
        created_after=created_after,
        created_before=created_before
    )
    
    # Get referrals
    referrals = review_service.get_referrals(current_company["id"], referral_filter, skip, limit)
    
    return referrals


@router.get("/referrals/{referral_id}", response_model=Referral)
async def get_referral(
    referral_id: str = Path(..., description="ID of the referral"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get a referral by ID.
    
    This endpoint retrieves a specific referral by ID.
    """
    referral = review_service.get_referral(current_company["id"], referral_id)
    
    if not referral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Referral with ID {referral_id} not found"
        )
    
    return referral


@router.post("/referrals/validate", response_model=Dict[str, Any])
async def validate_referral_code(
    code: str = Query(..., description="Referral code to validate"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Validate a referral code.
    
    This endpoint validates a referral code and returns the referral details if valid.
    """
    referral = review_service.validate_referral_code(current_company["id"], code)
    
    if not referral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Referral code {code} not found or invalid"
        )
    
    # Check if referral is active
    if referral.times_used >= referral.max_uses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referral code has reached maximum uses"
        )
    
    if referral.expires_at and referral.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referral code has expired"
        )
    
    return {
        "valid": True,
        "referral_id": referral.id,
        "code": referral.code,
        "offer_details": referral.offer_details,
        "times_used": referral.times_used,
        "max_uses": referral.max_uses,
        "expires_at": referral.expires_at
    }


@router.post("/referrals/{referral_id}/use", response_model=Referral)
async def use_referral(
    referral_id: str = Path(..., description="ID of the referral"),
    lead_id: str = Query(..., description="ID of the lead using the referral"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Use a referral for a lead.
    
    This endpoint marks a referral as used by a specific lead.
    """
    referral = review_service.use_referral(current_company["id"], referral_id, lead_id)
    
    if not referral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Referral with ID {referral_id} not found"
        )
    
    return referral

