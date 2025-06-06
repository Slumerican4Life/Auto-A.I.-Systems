"""
Content Generation API Routes

This module contains the API routes for the Content Generation Bot workflow.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from core.security import get_current_user
from workflows.content_generation.service import content_generation_service

router = APIRouter(
    prefix="/api/workflows/content-generation",
    tags=["content-generation"],
    responses={404: {"description": "Not found"}},
)

class BlogPostRequest(BaseModel):
    """Blog post generation request model."""
    topic: str
    word_count: Optional[int] = None
    keywords: Optional[str] = None
    call_to_action: Optional[str] = None

class SocialMediaRequest(BaseModel):
    """Social media post generation request model."""
    topic: str
    platform: str
    hashtags: Optional[str] = None
    call_to_action: Optional[str] = None

class EmailNewsletterRequest(BaseModel):
    """Email newsletter generation request model."""
    topic: str
    newsletter_type: Optional[str] = None
    content_sections: Optional[str] = None
    primary_goal: Optional[str] = None
    call_to_action: Optional[str] = None
    word_count: Optional[int] = None

class ProductDescriptionRequest(BaseModel):
    """Product description generation request model."""
    product_name: str
    product_category: Optional[str] = None
    key_features: Optional[str] = None
    primary_benefits: Optional[str] = None
    technical_specifications: Optional[str] = None
    price_point: Optional[str] = None
    unique_selling_proposition: Optional[str] = None
    platform: Optional[str] = None
    keywords: Optional[str] = None

class ContentScheduleRequest(BaseModel):
    """Content schedule request model."""
    content_type: str
    frequency: str
    day_of_week: Optional[str] = None
    time_of_day: Optional[str] = None
    topics: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
    active: Optional[bool] = True

class PublishContentRequest(BaseModel):
    """Publish content request model."""
    platform: str

@router.post("/blog-post")
async def generate_blog_post(
    request: BlogPostRequest,
    company_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate a blog post.
    
    Args:
        request: Blog post generation request
        company_id: ID of the company
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        content_generation_service.generate_blog_post,
        company_id,
        request.topic,
        word_count=request.word_count,
        keywords=request.keywords,
        call_to_action=request.call_to_action
    )
    
    return {
        "message": f"Generating blog post on topic '{request.topic}' in the background",
        "status": "pending"
    }

@router.post("/social-media")
async def generate_social_media_post(
    request: SocialMediaRequest,
    company_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate a social media post.
    
    Args:
        request: Social media post generation request
        company_id: ID of the company
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        content_generation_service.generate_social_media_post,
        company_id,
        request.topic,
        request.platform,
        hashtags=request.hashtags,
        call_to_action=request.call_to_action
    )
    
    return {
        "message": f"Generating {request.platform} post on topic '{request.topic}' in the background",
        "status": "pending"
    }

@router.post("/email-newsletter")
async def generate_email_newsletter(
    request: EmailNewsletterRequest,
    company_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate an email newsletter.
    
    Args:
        request: Email newsletter generation request
        company_id: ID of the company
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        content_generation_service.generate_email_newsletter,
        company_id,
        request.topic,
        newsletter_type=request.newsletter_type,
        content_sections=request.content_sections,
        primary_goal=request.primary_goal,
        call_to_action=request.call_to_action,
        word_count=request.word_count
    )
    
    return {
        "message": f"Generating email newsletter on topic '{request.topic}' in the background",
        "status": "pending"
    }

@router.post("/product-description")
async def generate_product_description(
    request: ProductDescriptionRequest,
    company_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate a product description.
    
    Args:
        request: Product description generation request
        company_id: ID of the company
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        content_generation_service.generate_product_description,
        company_id,
        request.product_name,
        product_category=request.product_category,
        key_features=request.key_features,
        primary_benefits=request.primary_benefits,
        technical_specifications=request.technical_specifications,
        price_point=request.price_point,
        unique_selling_proposition=request.unique_selling_proposition,
        platform=request.platform,
        keywords=request.keywords
    )
    
    return {
        "message": f"Generating product description for '{request.product_name}' in the background",
        "status": "pending"
    }

@router.post("/schedule")
async def schedule_content_generation(
    request: ContentScheduleRequest,
    company_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Schedule content generation based on a recurring schedule.
    
    Args:
        request: Content schedule request
        company_id: ID of the company
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    result = await content_generation_service.schedule_content_generation(
        company_id,
        {
            'content_type': request.content_type,
            'frequency': request.frequency,
            'day_of_week': request.day_of_week,
            'time_of_day': request.time_of_day,
            'topics': request.topics,
            'parameters': request.parameters,
            'active': request.active
        }
    )
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result['message']
        )
    
    return result

@router.post("/publish/{content_id}")
async def publish_content(
    content_id: str,
    request: PublishContentRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Publish content to a specified platform.
    
    Args:
        content_id: ID of the content to publish
        request: Publish content request
        background_tasks: FastAPI background tasks
        current_user: Current authenticated user
        
    Returns:
        Result of the operation
    """
    # Add task to background to avoid blocking the API
    background_tasks.add_task(
        content_generation_service.publish_content,
        content_id,
        request.platform
    )
    
    return {
        "message": f"Publishing content {content_id} to {request.platform} in the background",
        "status": "pending"
    }

@router.get("/content/{content_id}")
async def get_content(
    content_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get content by ID.
    
    Args:
        content_id: ID of the content to retrieve
        current_user: Current authenticated user
        
    Returns:
        Content data
    """
    # TODO: Implement content retrieval logic
    
    return {
        "message": f"Content {content_id} retrieved successfully",
        "content": {
            "id": content_id,
            "title": "Sample Content",
            "content": "This is sample content.",
            "status": "draft"
        }
    }

@router.get("/schedules")
async def get_content_schedules(
    company_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get content generation schedules for a company.
    
    Args:
        company_id: ID of the company
        current_user: Current authenticated user
        
    Returns:
        List of content generation schedules
    """
    # TODO: Implement schedule retrieval logic
    
    return {
        "message": "Content generation schedules retrieved successfully",
        "schedules": [
            {
                "id": "sample-schedule-id",
                "content_type": "blog_post",
                "frequency": "weekly",
                "day_of_week": "Monday",
                "time_of_day": "09:00",
                "active": True
            }
        ]
    }

