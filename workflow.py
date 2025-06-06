"""
Workflow models for the Business Automation System.

This module provides the data models for workflow configuration and management.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class WorkflowBase(BaseModel):
    """Base workflow model."""
    name: str
    type: str  # lead_nurturing, review_referral, content_generation
    description: Optional[str] = None
    is_active: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowCreate(WorkflowBase):
    """Workflow creation model."""
    id: Optional[str] = None
    company_id: Optional[str] = None
    created_at: Optional[datetime] = None


class WorkflowUpdate(BaseModel):
    """Workflow update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class Workflow(WorkflowBase):
    """Workflow model."""
    id: str
    company_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class WorkflowStep(BaseModel):
    """Workflow step model."""
    id: str
    workflow_id: str
    name: str
    type: str  # trigger, action, condition
    config: Dict[str, Any] = Field(default_factory=dict)
    position: int
    next_steps: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config."""
        orm_mode = True


class WorkflowExecution(BaseModel):
    """Workflow execution model."""
    id: str
    workflow_id: str
    company_id: str
    status: str  # running, completed, failed
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_step_id: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    result: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class WorkflowWithSteps(Workflow):
    """Workflow model with steps."""
    steps: List[WorkflowStep] = Field(default_factory=list)


class LeadNurturingWorkflowConfig(BaseModel):
    """Lead nurturing workflow configuration."""
    auto_followup: bool = True
    followup_delay_hours: int = 24
    final_followup_delay_hours: int = 72
    message_templates: Dict[str, str] = Field(default_factory=dict)
    default_channel: str = "email"  # email, sms
    lead_sources: List[str] = Field(default_factory=list)
    lead_statuses: List[str] = Field(default_factory=list)


class ReviewReferralWorkflowConfig(BaseModel):
    """Review and referral workflow configuration."""
    auto_referral: bool = True
    review_platforms: List[str] = Field(default_factory=list)
    review_request_delay_days: int = 3
    referral_offer: str = "10% discount for you and your friend"
    referral_max_uses: int = 3
    referral_expiry_days: int = 90
    message_templates: Dict[str, str] = Field(default_factory=dict)


class ContentGenerationWorkflowConfig(BaseModel):
    """Content generation workflow configuration."""
    content_types: List[str] = Field(default_factory=list)
    publishing_platforms: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    schedule: Dict[str, Any] = Field(default_factory=dict)
    topics: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    tone: str = "professional"

