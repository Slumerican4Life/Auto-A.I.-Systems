"""
Review Service for Business Automation System.

This module provides the service layer for review and referral management.
"""

import uuid
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from models.review_referral import (
    Review, ReviewRequestCreate, ReviewUpdate, ReviewFilter,
    Referral, ReferralCreate, ReferralFilter, Customer
)
from services.ai.ai_service import AIService
from services.email.email_service import EmailService
from services.sms.sms_service import SMSService
from services.analytics.analytics_service import AnalyticsService


class ReviewService:
    """Service for review and referral management."""

    def __init__(self):
        """Initialize the review service."""
        self.ai_service = AIService()
        self.email_service = EmailService()
        self.sms_service = SMSService()
        self.analytics_service = AnalyticsService()

    def get_customer(self, company_id: str, customer_id: str) -> Optional[Customer]:
        """
        Get a customer by ID.
        
        Args:
            company_id: ID of the company
            customer_id: ID of the customer
            
        Returns:
            Customer or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock customer
        if customer_id == "mock_customer_id":
            return Customer(
                id=customer_id,
                company_id=company_id,
                name="John Doe",
                email="john.doe@example.com",
                phone="+1234567890",
                created_at=datetime.utcnow() - timedelta(days=30),
                metadata={}
            )
        
        return None

    def create_review_request(self, review_request: ReviewRequestCreate) -> Review:
        """
        Create a new review request.
        
        Args:
            review_request: Review request creation data
            
        Returns:
            Created review request
        """
        # Generate ID if not provided
        if not review_request.id:
            review_request.id = str(uuid.uuid4())
        
        # Set created_at if not provided
        if not review_request.created_at:
            review_request.created_at = datetime.utcnow()
        
        # Set status to "requested" if not provided
        if not review_request.status:
            review_request.status = "requested"
        
        # In a real implementation, this would save to the database
        # For now, we'll just return a mock review
        review = Review(
            id=review_request.id,
            company_id=review_request.company_id,
            customer_id=review_request.customer_id,
            platform=review_request.platform,
            status=review_request.status,
            request_message=review_request.request_message,
            review_url=review_request.review_url,
            rating=None,
            review_content=None,
            created_at=review_request.created_at,
            completed_at=None,
            metadata=review_request.metadata or {}
        )
        
        return review

    def get_reviews(self, company_id: str, review_filter: ReviewFilter, skip: int = 0, limit: int = 100) -> List[Review]:
        """
        Get reviews with optional filtering.
        
        Args:
            company_id: ID of the company
            review_filter: Filter criteria
            skip: Number of reviews to skip
            limit: Maximum number of reviews to return
            
        Returns:
            List of reviews
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock list of reviews
        reviews = [
            Review(
                id=str(uuid.uuid4()),
                company_id=company_id,
                customer_id="customer1",
                platform="google",
                status="requested",
                request_message="We'd love your feedback on Google!",
                review_url="https://g.page/r/review-link",
                rating=None,
                review_content=None,
                created_at=datetime.utcnow() - timedelta(days=2),
                completed_at=None,
                metadata={}
            ),
            Review(
                id=str(uuid.uuid4()),
                company_id=company_id,
                customer_id="customer2",
                platform="yelp",
                status="completed",
                request_message="We'd love your feedback on Yelp!",
                review_url="https://yelp.com/review-link",
                rating=5,
                review_content="Great service, highly recommended!",
                created_at=datetime.utcnow() - timedelta(days=5),
                completed_at=datetime.utcnow() - timedelta(days=4),
                metadata={}
            )
        ]
        
        # Apply filters
        filtered_reviews = reviews
        if review_filter.status:
            filtered_reviews = [review for review in filtered_reviews if review.status == review_filter.status]
        if review_filter.platform:
            filtered_reviews = [review for review in filtered_reviews if review.platform == review_filter.platform]
        if review_filter.rating:
            filtered_reviews = [review for review in filtered_reviews if review.rating == review_filter.rating]
        if review_filter.created_after:
            filtered_reviews = [review for review in filtered_reviews if review.created_at >= review_filter.created_after]
        if review_filter.created_before:
            filtered_reviews = [review for review in filtered_reviews if review.created_at <= review_filter.created_before]
        
        # Apply pagination
        paginated_reviews = filtered_reviews[skip:skip + limit]
        
        return paginated_reviews

    def get_review(self, company_id: str, review_id: str) -> Optional[Review]:
        """
        Get a review by ID.
        
        Args:
            company_id: ID of the company
            review_id: ID of the review
            
        Returns:
            Review or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock review
        if review_id == "mock_review_id":
            return Review(
                id=review_id,
                company_id=company_id,
                customer_id="customer1",
                platform="google",
                status="requested",
                request_message="We'd love your feedback on Google!",
                review_url="https://g.page/r/review-link",
                rating=None,
                review_content=None,
                created_at=datetime.utcnow() - timedelta(days=2),
                completed_at=None,
                metadata={}
            )
        
        return None

    def update_review(self, company_id: str, review_id: str, review_update: ReviewUpdate) -> Review:
        """
        Update a review.
        
        Args:
            company_id: ID of the company
            review_id: ID of the review
            review_update: Review update data
            
        Returns:
            Updated review
        """
        # In a real implementation, this would update the database
        # For now, we'll just return a mock updated review
        review = self.get_review(company_id, review_id)
        
        if not review:
            # In a real implementation, this would raise an exception
            # For now, we'll just return a mock review
            review = Review(
                id=review_id,
                company_id=company_id,
                customer_id="customer1",
                platform="google",
                status="requested",
                request_message="We'd love your feedback on Google!",
                review_url="https://g.page/r/review-link",
                rating=None,
                review_content=None,
                created_at=datetime.utcnow() - timedelta(days=2),
                completed_at=None,
                metadata={}
            )
        
        # Update fields
        if review_update.status:
            review.status = review_update.status
            
            # If status is changed to completed, set completed_at
            if review_update.status == "completed" and not review.completed_at:
                review.completed_at = datetime.utcnow()
        
        if review_update.rating is not None:
            review.rating = review_update.rating
        
        if review_update.review_content:
            review.review_content = review_update.review_content
        
        if review_update.metadata:
            review.metadata = {**review.metadata, **review_update.metadata}
        
        return review

    def generate_referral_code(self, company_id: str, customer_id: str) -> str:
        """
        Generate a unique referral code for a customer.
        
        Args:
            company_id: ID of the company
            customer_id: ID of the customer
            
        Returns:
            Generated referral code
        """
        # Generate a random code
        code_length = 8
        code_chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(code_chars) for _ in range(code_length))
        
        # In a real implementation, we would check if the code already exists
        # and generate a new one if it does
        
        return code

    def create_referral(self, referral_create: ReferralCreate, referral_code: str) -> Referral:
        """
        Create a new referral.
        
        Args:
            referral_create: Referral creation data
            referral_code: Generated referral code
            
        Returns:
            Created referral
        """
        # Generate ID if not provided
        if not referral_create.id:
            referral_create.id = str(uuid.uuid4())
        
        # Set created_at if not provided
        if not referral_create.created_at:
            referral_create.created_at = datetime.utcnow()
        
        # In a real implementation, this would save to the database
        # For now, we'll just return a mock referral
        referral = Referral(
            id=referral_create.id,
            company_id=referral_create.company_id,
            customer_id=referral_create.customer_id,
            code=referral_code,
            offer_details=referral_create.offer_details,
            max_uses=referral_create.max_uses,
            times_used=0,
            created_at=referral_create.created_at,
            expires_at=referral_create.expires_at or (datetime.utcnow() + timedelta(days=90)),
            metadata=referral_create.metadata or {}
        )
        
        return referral

    def get_referrals(self, company_id: str, referral_filter: ReferralFilter, skip: int = 0, limit: int = 100) -> List[Referral]:
        """
        Get referrals with optional filtering.
        
        Args:
            company_id: ID of the company
            referral_filter: Filter criteria
            skip: Number of referrals to skip
            limit: Maximum number of referrals to return
            
        Returns:
            List of referrals
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock list of referrals
        referrals = [
            Referral(
                id=str(uuid.uuid4()),
                company_id=company_id,
                customer_id="customer1",
                code="ABC123XY",
                offer_details="10% discount for you and your friend",
                max_uses=3,
                times_used=0,
                created_at=datetime.utcnow() - timedelta(days=2),
                expires_at=datetime.utcnow() + timedelta(days=88),
                metadata={}
            ),
            Referral(
                id=str(uuid.uuid4()),
                company_id=company_id,
                customer_id="customer2",
                code="DEF456ZW",
                offer_details="10% discount for you and your friend",
                max_uses=3,
                times_used=1,
                created_at=datetime.utcnow() - timedelta(days=10),
                expires_at=datetime.utcnow() + timedelta(days=80),
                metadata={}
            )
        ]
        
        # Apply filters
        filtered_referrals = referrals
        if referral_filter.status:
            if referral_filter.status == "active":
                filtered_referrals = [
                    referral for referral in filtered_referrals 
                    if referral.times_used < referral.max_uses and referral.expires_at > datetime.utcnow()
                ]
            elif referral_filter.status == "expired":
                filtered_referrals = [
                    referral for referral in filtered_referrals 
                    if referral.expires_at <= datetime.utcnow()
                ]
            elif referral_filter.status == "used":
                filtered_referrals = [
                    referral for referral in filtered_referrals 
                    if referral.times_used >= referral.max_uses
                ]
        
        if referral_filter.customer_id:
            filtered_referrals = [
                referral for referral in filtered_referrals 
                if referral.customer_id == referral_filter.customer_id
            ]
        
        if referral_filter.created_after:
            filtered_referrals = [
                referral for referral in filtered_referrals 
                if referral.created_at >= referral_filter.created_after
            ]
        
        if referral_filter.created_before:
            filtered_referrals = [
                referral for referral in filtered_referrals 
                if referral.created_at <= referral_filter.created_before
            ]
        
        # Apply pagination
        paginated_referrals = filtered_referrals[skip:skip + limit]
        
        return paginated_referrals

    def get_referral(self, company_id: str, referral_id: str) -> Optional[Referral]:
        """
        Get a referral by ID.
        
        Args:
            company_id: ID of the company
            referral_id: ID of the referral
            
        Returns:
            Referral or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock referral
        if referral_id == "mock_referral_id":
            return Referral(
                id=referral_id,
                company_id=company_id,
                customer_id="customer1",
                code="ABC123XY",
                offer_details="10% discount for you and your friend",
                max_uses=3,
                times_used=0,
                created_at=datetime.utcnow() - timedelta(days=2),
                expires_at=datetime.utcnow() + timedelta(days=88),
                metadata={}
            )
        
        return None

    def validate_referral_code(self, company_id: str, code: str) -> Optional[Referral]:
        """
        Validate a referral code.
        
        Args:
            company_id: ID of the company
            code: Referral code
            
        Returns:
            Referral or None if not valid
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock referral if the code matches
        if code == "ABC123XY":
            return Referral(
                id="mock_referral_id",
                company_id=company_id,
                customer_id="customer1",
                code=code,
                offer_details="10% discount for you and your friend",
                max_uses=3,
                times_used=0,
                created_at=datetime.utcnow() - timedelta(days=2),
                expires_at=datetime.utcnow() + timedelta(days=88),
                metadata={}
            )
        
        return None

    def use_referral(self, company_id: str, referral_id: str, lead_id: str) -> Referral:
        """
        Use a referral for a lead.
        
        Args:
            company_id: ID of the company
            referral_id: ID of the referral
            lead_id: ID of the lead
            
        Returns:
            Updated referral
        """
        # In a real implementation, this would update the database
        # For now, we'll just return a mock updated referral
        referral = self.get_referral(company_id, referral_id)
        
        if not referral:
            # In a real implementation, this would raise an exception
            return None
        
        # Increment times_used
        referral.times_used += 1
        
        # Add lead_id to metadata
        if "used_by" not in referral.metadata:
            referral.metadata["used_by"] = []
        
        referral.metadata["used_by"].append({
            "lead_id": lead_id,
            "used_at": datetime.utcnow().isoformat()
        })
        
        return referral

