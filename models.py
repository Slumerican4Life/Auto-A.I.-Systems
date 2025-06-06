from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, EmailStr

class LeadBase(BaseModel):
    """Base model for lead data"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    source: str
    notes: Optional[str] = None
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}

class LeadCreate(LeadBase):
    """Model for creating a new lead"""
    company_id: str
    assigned_to: Optional[str] = None

class LeadUpdate(BaseModel):
    """Model for updating an existing lead"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

class LeadInDB(LeadBase):
    """Model for a lead stored in the database"""
    id: str
    company_id: str
    status: str = "new"
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None

class Lead(LeadInDB):
    """Model for a lead returned to the client"""
    interactions: Optional[List[Dict[str, Any]]] = None

class InteractionBase(BaseModel):
    """Base model for interaction data"""
    lead_id: str
    type: str  # email, sms, call, meeting
    direction: str  # outbound, inbound
    content: str
    channel: str  # automated_workflow, manual, reply
    status: str  # delivered, opened, clicked, replied

class InteractionCreate(InteractionBase):
    """Model for creating a new interaction"""
    company_id: str
    created_by: Optional[str] = None
    metadata: Dict[str, Any] = {}

class InteractionInDB(InteractionBase):
    """Model for an interaction stored in the database"""
    id: str
    company_id: str
    created_at: datetime
    created_by: Optional[str] = None
    metadata: Dict[str, Any] = {}

class Interaction(InteractionInDB):
    """Model for an interaction returned to the client"""
    pass

class LeadNurturingConfig(BaseModel):
    """Configuration for lead nurturing workflow"""
    id: Optional[str] = None
    company_id: str
    name: str
    active: bool = True
    triggers: Dict[str, Any]
    actions: Dict[str, Any]
    templates: Dict[str, str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None

class LeadNurturingRun(BaseModel):
    """Record of a lead nurturing workflow run"""
    id: Optional[str] = None
    company_id: str
    workflow_config_id: str
    status: str = "pending"  # pending, running, completed, failed
    started_at: datetime
    completed_at: Optional[datetime] = None
    trigger_type: str
    trigger_id: str
    actions_performed: List[Dict[str, Any]] = []
    results: Dict[str, Any] = {}
    error: Optional[str] = None

