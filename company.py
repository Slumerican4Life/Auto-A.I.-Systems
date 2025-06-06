"""
Company models for the Business Automation System.

This module provides the data models for companies.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class CompanyBase(BaseModel):
    """Base company model."""
    name: str
    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None


class CompanyCreate(CompanyBase):
    """Company creation model."""
    owner_email: EmailStr


class CompanyUpdate(BaseModel):
    """Company update model."""
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None


class CompanyInDBBase(CompanyBase):
    """Company in database model."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: str
    is_active: bool = True
    subscription_plan: str = "free"
    subscription_expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""
        orm_mode = True


class Company(CompanyInDBBase):
    """Company model."""
    pass


class CompanyWithUsers(Company):
    """Company model with users."""
    users: List[Dict[str, Any]] = []


class CompanySettings(BaseModel):
    """Company settings model."""
    company_id: str
    email_templates: Dict[str, Any] = Field(default_factory=dict)
    sms_templates: Dict[str, Any] = Field(default_factory=dict)
    lead_sources: List[str] = Field(default_factory=list)
    review_platforms: List[str] = Field(default_factory=list)
    content_types: List[str] = Field(default_factory=list)
    workflow_settings: Dict[str, Any] = Field(default_factory=dict)
    branding: Dict[str, Any] = Field(default_factory=dict)
    integrations: Dict[str, Any] = Field(default_factory=dict)


class CompanySubscription(BaseModel):
    """Company subscription model."""
    company_id: str
    plan: str
    status: str
    starts_at: datetime
    expires_at: Optional[datetime] = None
    payment_method: Optional[str] = None
    auto_renew: bool = True
    features: Dict[str, Any] = Field(default_factory=dict)
    limits: Dict[str, int] = Field(default_factory=dict)

