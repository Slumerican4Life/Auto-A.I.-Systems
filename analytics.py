"""
API router for analytics.

This module provides the API endpoints for retrieving analytics and metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from models.analytics import (
    AnalyticsFilter, DashboardMetrics, LeadMetrics,
    ReviewMetrics, ReferralMetrics, ContentMetrics
)
from services.analytics.analytics_service import AnalyticsService
from core.security import get_current_user, get_current_company

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get metrics for the dashboard.
    
    This endpoint retrieves metrics for the dashboard, including summary metrics,
    charts, and value summary.
    """
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get dashboard metrics
    metrics = analytics_service.get_dashboard_metrics(current_company["id"], start_date, end_date)
    
    return metrics


@router.get("/leads", response_model=Dict[str, Any])
async def get_lead_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    source: Optional[str] = Query(None, description="Filter by lead source"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get lead-related metrics.
    
    This endpoint retrieves metrics related to leads, including conversion rates,
    sources, and response times.
    """
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get lead metrics
    metrics = analytics_service.get_lead_metrics(current_company["id"], start_date, end_date, source)
    
    return metrics


@router.get("/reviews", response_model=Dict[str, Any])
async def get_review_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    platform: Optional[str] = Query(None, description="Filter by review platform"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get review-related metrics.
    
    This endpoint retrieves metrics related to reviews, including completion rates,
    platforms, and rating distribution.
    """
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get review metrics
    metrics = analytics_service.get_review_metrics(current_company["id"], start_date, end_date, platform)
    
    return metrics


@router.get("/referrals", response_model=Dict[str, Any])
async def get_referral_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get referral-related metrics.
    
    This endpoint retrieves metrics related to referrals, including usage rates,
    conversion rates, and top referrers.
    """
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get referral metrics
    metrics = analytics_service.get_referral_metrics(current_company["id"], start_date, end_date)
    
    return metrics


@router.get("/content", response_model=Dict[str, Any])
async def get_content_metrics(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get content-related metrics.
    
    This endpoint retrieves metrics related to content, including engagement rates,
    content types, and top performing content.
    """
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get content metrics
    metrics = analytics_service.get_content_metrics(current_company["id"], start_date, end_date, content_type)
    
    return metrics


@router.get("/activity", response_model=List[Dict[str, Any]])
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of activities to return"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get recent activity.
    
    This endpoint retrieves recent activity for the company.
    """
    # Get recent activity
    activities = analytics_service.get_recent_activity(current_company["id"], limit)
    
    return activities


@router.post("/track/lead", response_model=Dict[str, Any])
async def track_lead_metric(
    lead_id: str = Query(..., description="ID of the lead"),
    status: str = Query(..., description="Lead status"),
    source: Optional[str] = Query(None, description="Lead source"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Track a lead metric.
    
    This endpoint tracks a lead-related metric.
    """
    # Track metric
    result = analytics_service.track_lead_metric(current_company["id"], lead_id, status, source)
    
    return result


@router.post("/track/review", response_model=Dict[str, Any])
async def track_review_metric(
    customer_id: str = Query(..., description="ID of the customer"),
    status: str = Query(..., description="Review status"),
    platform: Optional[str] = Query(None, description="Review platform"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="Review rating"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Track a review metric.
    
    This endpoint tracks a review-related metric.
    """
    # Track metric
    result = analytics_service.track_review_metric(current_company["id"], customer_id, status, platform, rating)
    
    return result


@router.post("/track/referral", response_model=Dict[str, Any])
async def track_referral_metric(
    referral_id: str = Query(..., description="ID of the referral"),
    status: str = Query(..., description="Referral status"),
    customer_id: Optional[str] = Query(None, description="ID of the customer who created the referral"),
    referred_lead_id: Optional[str] = Query(None, description="ID of the lead who used the referral"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Track a referral metric.
    
    This endpoint tracks a referral-related metric.
    """
    # Track metric
    result = analytics_service.track_referral_metric(current_company["id"], referral_id, status, customer_id, referred_lead_id)
    
    return result


@router.post("/track/content", response_model=Dict[str, Any])
async def track_content_metric(
    content_id: str = Query(..., description="ID of the content"),
    status: str = Query(..., description="Content status"),
    content_type: Optional[str] = Query(None, description="Content type"),
    platform: Optional[str] = Query(None, description="Publishing platform"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Track a content metric.
    
    This endpoint tracks a content-related metric.
    """
    # Track metric
    result = analytics_service.track_content_metric(current_company["id"], content_id, status, content_type, platform)
    
    return result


@router.post("/track/content/engagement", response_model=Dict[str, Any])
async def track_content_engagement(
    content_id: str = Query(..., description="ID of the content"),
    engagement_type: str = Query(..., description="Type of engagement (view, click, share, comment, like)"),
    value: int = Query(1, ge=1, description="Engagement value"),
    platform: Optional[str] = Query(None, description="Publishing platform"),
    metadata: Optional[Dict[str, Any]] = Body({}, description="Additional metadata"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Track content engagement.
    
    This endpoint tracks content engagement metrics.
    """
    # Track engagement
    result = analytics_service.track_content_engagement(current_company["id"], content_id, engagement_type, value, platform, metadata)
    
    return result

