"""
Lead models for the Business Automation System.

This module provides the data models for leads and interactions.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field


class LeadBase(BaseModel):
    """Base lead model."""
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = "new"
    assigned_to: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LeadCreate(LeadBase):
    """Lead creation model."""
    id: Optional[str] = None
    company_id: Optional[str] = None
    created_at: Optional[datetime] = None
    auto_followup: bool = False


class LeadUpdate(BaseModel):
    """Lead update model."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class LeadFilter(BaseModel):
    """Lead filter model."""
    status: Optional[str] = None
    source: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None


class Lead(LeadBase):
    """Lead model."""
    id: str
    company_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class InteractionBase(BaseModel):
    """Base interaction model."""
    type: str  # email, sms, call, meeting, note
    direction: str  # inbound, outbound
    content: str
    channel: str  # manual, automated, api
    created_by: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InteractionCreate(InteractionBase):
    """Interaction creation model."""
    id: Optional[str] = None
    company_id: Optional[str] = None
    lead_id: Optional[str] = None
    created_at: Optional[datetime] = None


class Interaction(InteractionBase):
    """Interaction model."""
    id: str
    company_id: str
    lead_id: str
    created_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class LeadWithInteractions(Lead):
    """Lead model with interactions."""
    interactions: List[Interaction] = Field(default_factory=list)

