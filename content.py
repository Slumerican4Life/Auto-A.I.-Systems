"""
API router for content management.

This module provides the API endpoints for managing content generation and publishing.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from models.content import (
    Content, ContentCreate, ContentUpdate, ContentFilter,
    ContentGenerateRequest, ContentPublishRequest
)
from services.content_service import ContentService
from services.ai.ai_service import AIService
from services.scheduler.scheduler_service import SchedulerService
from core.security import get_current_user, get_current_company

router = APIRouter()
content_service = ContentService()
ai_service = AIService()
scheduler_service = SchedulerService()


@router.post("/", response_model=Content, status_code=status.HTTP_201_CREATED)
async def create_content(
    content_in: ContentCreate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Create new content.
    
    This endpoint creates new content in the system.
    """
    # Set company ID from authenticated user
    content_in.company_id = current_company["id"]
    
    # Create content
    content = content_service.create_content(content_in, current_user["id"])
    
    return content


@router.get("/", response_model=List[Content])
async def get_content_list(
    status: Optional[str] = Query(None, description="Filter by content status"),
    type: Optional[str] = Query(None, description="Filter by content type"),
    platform: Optional[str] = Query(None, description="Filter by publishing platform"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    created_after: Optional[datetime] = Query(None, description="Filter by creation date (after)"),
    created_before: Optional[datetime] = Query(None, description="Filter by creation date (before)"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    skip: int = Query(0, ge=0, description="Number of content items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of content items to return"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get content with optional filtering.
    
    This endpoint retrieves content with optional filtering criteria.
    """
    # Create filter
    content_filter = ContentFilter(
        status=status,
        type=type,
        platform=platform,
        tags=tags,
        created_after=created_after,
        created_before=created_before,
        created_by=created_by
    )
    
    # Get content
    content_list = content_service.get_content_list(current_company["id"], content_filter, skip, limit)
    
    return content_list


@router.get("/{content_id}", response_model=Content)
async def get_content(
    content_id: str = Path(..., description="ID of the content"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Get content by ID.
    
    This endpoint retrieves specific content by ID.
    """
    content = content_service.get_content(current_company["id"], content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    return content


@router.put("/{content_id}", response_model=Content)
async def update_content(
    content_id: str = Path(..., description="ID of the content"),
    content_update: ContentUpdate = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Update content.
    
    This endpoint updates specific content by ID.
    """
    content = content_service.update_content(current_company["id"], content_id, content_update)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: str = Path(..., description="ID of the content"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Delete content.
    
    This endpoint deletes specific content by ID.
    """
    success = content_service.delete_content(current_company["id"], content_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    return None


@router.post("/generate", response_model=Dict[str, Any])
async def generate_content(
    request: ContentGenerateRequest = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Generate content using AI.
    
    This endpoint generates content using AI based on the provided parameters.
    """
    # Generate content
    generated_content = ai_service.generate_content(
        content_type=request.content_type,
        topic=request.topic,
        keywords=request.keywords,
        tone=request.tone,
        length=request.length,
        target_audience=request.target_audience,
        additional_instructions=request.additional_instructions,
        company_id=current_company["id"]
    )
    
    # Create content in the system if save_to_library is true
    content = None
    if request.save_to_library:
        content_in = ContentCreate(
            company_id=current_company["id"],
            title=generated_content["title"],
            type=request.content_type,
            body=generated_content["body"],
            tags=request.keywords or [],
            status="draft",
            platform=request.platform
        )
        
        content = content_service.create_content(content_in, current_user["id"])
    
    return {
        "success": True,
        "content": generated_content,
        "saved_content_id": content.id if content else None
    }


@router.post("/{content_id}/publish", response_model=Dict[str, Any])
async def publish_content(
    content_id: str = Path(..., description="ID of the content"),
    request: ContentPublishRequest = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Publish content to a platform.
    
    This endpoint publishes content to a specified platform.
    """
    # Get content
    content = content_service.get_content(current_company["id"], content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    # Publish content
    result = content_service.publish_content(
        company_id=current_company["id"],
        content_id=content_id,
        platform=request.platform,
        params=request.params
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to publish content")
        )
    
    # Update content status and platform
    content_service.update_content(
        company_id=current_company["id"],
        content_id=content_id,
        content_update=ContentUpdate(
            status="published",
            platform=request.platform,
            url=result.get("url"),
            published_at=datetime.utcnow(),
            metadata={
                "publish_result": result
            }
        )
    )
    
    return {
        "success": True,
        "content_id": content_id,
        "platform": request.platform,
        "url": result.get("url"),
        "published_at": result.get("published_at")
    }


@router.post("/schedule", response_model=Dict[str, Any])
async def schedule_content_generation(
    content_type: str = Query(..., description="Type of content to generate"),
    topic: str = Query(..., description="Topic for the content"),
    frequency: str = Query("weekly", description="Frequency of generation (daily, weekly, monthly)"),
    day_of_week: Optional[int] = Query(None, ge=0, le=6, description="Day of week for weekly schedule (0=Monday, 6=Sunday)"),
    day_of_month: Optional[int] = Query(None, ge=1, le=31, description="Day of month for monthly schedule"),
    hour: int = Query(9, ge=0, le=23, description="Hour of day for generation (24-hour format)"),
    minute: int = Query(0, ge=0, le=59, description="Minute of hour for generation"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    current_company: Dict[str, Any] = Depends(get_current_company)
):
    """
    Schedule recurring content generation.
    
    This endpoint schedules recurring content generation based on the provided parameters.
    """
    # Create schedule
    now = datetime.utcnow()
    start_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    schedule = {
        "frequency": frequency,
        "start_at": start_at.isoformat()
    }
    
    if frequency == "weekly" and day_of_week is not None:
        schedule["day_of_week"] = day_of_week
    
    if frequency == "monthly" and day_of_month is not None:
        schedule["day_of_month"] = day_of_month
    
    # Schedule content generation
    result = scheduler_service.schedule_content_generation(
        company_id=current_company["id"],
        content_type=content_type,
        topic=topic,
        schedule=schedule
    )
    
    return {
        "success": True,
        "task_id": result["task_id"],
        "content_type": content_type,
        "topic": topic,
        "schedule": schedule,
        "next_execution_at": result["next_execution_at"]
    }

