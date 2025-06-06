"""
User models for the Business Automation System.

This module provides the data models for users and authentication.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    company_id: str


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    """User in database model."""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class User(UserInDBBase):
    """User model."""
    pass


class UserInDB(UserInDBBase):
    """User in database model with hashed password."""
    hashed_password: str


class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""
    email: Optional[str] = None


class UserRole(BaseModel):
    """User role model."""
    id: str
    name: str
    permissions: List[str]


class UserWithRoles(User):
    """User model with roles."""
    roles: List[UserRole] = []

