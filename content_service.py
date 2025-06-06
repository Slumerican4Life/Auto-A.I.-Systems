"""
Content Service for Business Automation System.

This module provides the service layer for content management and generation.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from models.content import (
    Content, ContentCreate, ContentUpdate, ContentFilter,
    ContentGenerateRequest, ContentPublishRequest
)
from services.ai.ai_service import AIService
from services.analytics.analytics_service import AnalyticsService


class ContentService:
    """Service for content management and generation."""

    def __init__(self):
        """Initialize the content service."""
        self.ai_service = AIService()
        self.analytics_service = AnalyticsService()

    def create_content(self, content_in: ContentCreate, created_by: str) -> Content:
        """
        Create new content.
        
        Args:
            content_in: Content creation data
            created_by: ID of the user creating the content
            
        Returns:
            Created content
        """
        # Generate ID if not provided
        if not content_in.id:
            content_in.id = str(uuid.uuid4())
        
        # Set created_at if not provided
        if not content_in.created_at:
            content_in.created_at = datetime.utcnow()
        
        # Set status to "draft" if not provided
        if not content_in.status:
            content_in.status = "draft"
        
        # In a real implementation, this would save to the database
        # For now, we'll just return a mock content
        content = Content(
            id=content_in.id,
            company_id=content_in.company_id,
            title=content_in.title,
            type=content_in.type,
            body=content_in.body,
            tags=content_in.tags or [],
            status=content_in.status,
            platform=content_in.platform,
            url=content_in.url,
            created_by=created_by,
            created_at=content_in.created_at,
            published_at=None,
            metadata=content_in.metadata or {}
        )
        
        return content

    def get_content_list(self, company_id: str, content_filter: ContentFilter, skip: int = 0, limit: int = 100) -> List[Content]:
        """
        Get content with optional filtering.
        
        Args:
            company_id: ID of the company
            content_filter: Filter criteria
            skip: Number of content items to skip
            limit: Maximum number of content items to return
            
        Returns:
            List of content items
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock list of content
        content_list = [
            Content(
                id=str(uuid.uuid4()),
                company_id=company_id,
                title="10 Tips for Small Business Success",
                type="blog",
                body="Here are 10 tips for small business success...",
                tags=["small business", "tips", "success"],
                status="published",
                platform="wordpress",
                url="https://example.com/blog/10-tips",
                created_by="user123",
                created_at=datetime.utcnow() - timedelta(days=5),
                published_at=datetime.utcnow() - timedelta(days=4),
                metadata={}
            ),
            Content(
                id=str(uuid.uuid4()),
                company_id=company_id,
                title="New Product Announcement",
                type="email",
                body="We're excited to announce our new product...",
                tags=["product", "announcement", "email"],
                status="draft",
                platform=None,
                url=None,
                created_by="user123",
                created_at=datetime.utcnow() - timedelta(days=2),
                published_at=None,
                metadata={}
            )
        ]
        
        # Apply filters
        filtered_content = content_list
        if content_filter.status:
            filtered_content = [content for content in filtered_content if content.status == content_filter.status]
        if content_filter.type:
            filtered_content = [content for content in filtered_content if content.type == content_filter.type]
        if content_filter.platform:
            filtered_content = [content for content in filtered_content if content.platform == content_filter.platform]
        if content_filter.tags:
            filtered_content = [
                content for content in filtered_content 
                if any(tag in content.tags for tag in content_filter.tags)
            ]
        if content_filter.created_after:
            filtered_content = [
                content for content in filtered_content 
                if content.created_at >= content_filter.created_after
            ]
        if content_filter.created_before:
            filtered_content = [
                content for content in filtered_content 
                if content.created_at <= content_filter.created_before
            ]
        if content_filter.created_by:
            filtered_content = [
                content for content in filtered_content 
                if content.created_by == content_filter.created_by
            ]
        
        # Apply pagination
        paginated_content = filtered_content[skip:skip + limit]
        
        return paginated_content

    def get_content(self, company_id: str, content_id: str) -> Optional[Content]:
        """
        Get content by ID.
        
        Args:
            company_id: ID of the company
            content_id: ID of the content
            
        Returns:
            Content or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll just return a mock content
        if content_id == "mock_content_id":
            return Content(
                id=content_id,
                company_id=company_id,
                title="10 Tips for Small Business Success",
                type="blog",
                body="Here are 10 tips for small business success...",
                tags=["small business", "tips", "success"],
                status="published",
                platform="wordpress",
                url="https://example.com/blog/10-tips",
                created_by="user123",
                created_at=datetime.utcnow() - timedelta(days=5),
                published_at=datetime.utcnow() - timedelta(days=4),
                metadata={}
            )
        
        return None

    def update_content(self, company_id: str, content_id: str, content_update: ContentUpdate) -> Content:
        """
        Update content.
        
        Args:
            company_id: ID of the company
            content_id: ID of the content
            content_update: Content update data
            
        Returns:
            Updated content
        """
        # In a real implementation, this would update the database
        # For now, we'll just return a mock updated content
        content = self.get_content(company_id, content_id)
        
        if not content:
            # In a real implementation, this would raise an exception
            # For now, we'll just return a mock content
            content = Content(
                id=content_id,
                company_id=company_id,
                title="10 Tips for Small Business Success",
                type="blog",
                body="Here are 10 tips for small business success...",
                tags=["small business", "tips", "success"],
                status="draft",
                platform=None,
                url=None,
                created_by="user123",
                created_at=datetime.utcnow() - timedelta(days=2),
                published_at=None,
                metadata={}
            )
        
        # Update fields
        if content_update.title:
            content.title = content_update.title
        if content_update.body:
            content.body = content_update.body
        if content_update.tags:
            content.tags = content_update.tags
        if content_update.status:
            content.status = content_update.status
            
            # If status is changed to published, set published_at
            if content_update.status == "published" and not content.published_at:
                content.published_at = datetime.utcnow()
        
        if content_update.platform:
            content.platform = content_update.platform
        if content_update.url:
            content.url = content_update.url
        if content_update.metadata:
            content.metadata = {**content.metadata, **content_update.metadata}
        if content_update.published_at:
            content.published_at = content_update.published_at
        
        return content

    def delete_content(self, company_id: str, content_id: str) -> bool:
        """
        Delete content.
        
        Args:
            company_id: ID of the company
            content_id: ID of the content
            
        Returns:
            True if deleted, False otherwise
        """
        # In a real implementation, this would delete from the database
        # For now, we'll just return True
        return True

    def update_content_metadata(self, company_id: str, content_id: str, metadata_key: str, metadata_value: Any) -> Content:
        """
        Update content metadata.
        
        Args:
            company_id: ID of the company
            content_id: ID of the content
            metadata_key: Key to update
            metadata_value: Value to set
            
        Returns:
            Updated content
        """
        # In a real implementation, this would update the database
        # For now, we'll just return a mock updated content
        content = self.get_content(company_id, content_id)
        
        if not content:
            return None
        
        # Update metadata
        content.metadata[metadata_key] = metadata_value
        
        return content

    def publish_content(self, company_id: str, content_id: str, platform: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Publish content to a platform.
        
        Args:
            company_id: ID of the company
            content_id: ID of the content
            platform: Platform to publish to
            params: Additional parameters for publishing
            
        Returns:
            Dictionary with publish result
        """
        # In a real implementation, this would publish to the platform
        # For now, we'll just return a mock result
        content = self.get_content(company_id, content_id)
        
        if not content:
            return {"success": False, "error": "Content not found"}
        
        # Mock publishing to different platforms
        if platform == "wordpress":
            return {
                "success": True,
                "platform": "wordpress",
                "url": f"https://example.com/blog/{content_id}",
                "published_at": datetime.utcnow().isoformat()
            }
        elif platform == "buffer":
            return {
                "success": True,
                "platform": "buffer",
                "url": f"https://buffer.com/updates/{content_id}",
                "published_at": datetime.utcnow().isoformat()
            }
        elif platform == "email":
            return {
                "success": True,
                "platform": "email",
                "url": None,
                "published_at": datetime.utcnow().isoformat(),
                "recipients": params.get("recipients", 0)
            }
        else:
            return {
                "success": False,
                "error": f"Unsupported platform: {platform}"
            }

