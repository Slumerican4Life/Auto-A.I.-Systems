"""
API router for authentication.

This module provides the API endpoints for user authentication and authorization.
"""

from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any, Optional

from models.user import User, UserCreate, UserUpdate, Token
from core.security import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_user, get_current_active_user
)

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate = Body(...)):
    """
    Register a new user.
    
    This endpoint registers a new user in the system.
    """
    # In a real implementation, this would check if the user already exists
    # and save the new user to the database
    
    # Mock implementation for development
    hashed_password = get_password_hash(user_in.password)
    
    user = User(
        id="user123",
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False,
        company_id=user_in.company_id
    )
    
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token for authentication.
    
    This endpoint authenticates a user and returns an access token.
    """
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user.
    
    This endpoint returns the current authenticated user.
    """
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate = Body(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update current user.
    
    This endpoint updates the current authenticated user.
    """
    # In a real implementation, this would update the user in the database
    
    # Mock implementation for development
    updated_user = User(
        id=current_user.id,
        email=user_update.email or current_user.email,
        hashed_password=current_user.hashed_password,
        full_name=user_update.full_name or current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        company_id=current_user.company_id
    )
    
    return updated_user


@router.post("/password", response_model=Dict[str, Any])
async def change_password(
    old_password: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    current_user: User = Depends(get_current_active_user)
):
    """
    Change user password.
    
    This endpoint changes the password for the current authenticated user.
    """
    # In a real implementation, this would verify the old password
    # and update the password in the database
    
    # Mock implementation for development
    if not authenticate_user(current_user.email, old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    hashed_password = get_password_hash(new_password)
    
    return {
        "message": "Password changed successfully"
    }


@router.post("/logout", response_model=Dict[str, Any])
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout current user.
    
    This endpoint logs out the current authenticated user.
    """
    # In a real implementation, this would invalidate the token
    # or add it to a blacklist
    
    # Mock implementation for development
    return {
        "message": "Logged out successfully"
    }

