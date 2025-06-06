"""
Security module for the Business Automation System.

This module provides security-related functionality, including authentication,
authorization, and token management.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from models.user import User, TokenData

# Security settings
SECRET_KEY = os.environ.get("SECRET_KEY", "mock_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        User if authentication is successful, None otherwise
    """
    # In a real implementation, this would query the database
    # For now, we'll just use a mock user
    
    # Mock user for development
    if email == "user@example.com" and password == "password":
        return User(
            id="user123",
            email="user@example.com",
            hashed_password=get_password_hash("password"),
            full_name="John Doe",
            is_active=True,
            is_superuser=False,
            company_id="company123"
        )
    
    return None


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user.
    
    Args:
        token: JWT token
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # In a real implementation, this would query the database
    # For now, we'll just use a mock user
    
    # Mock user for development
    if token_data.email == "user@example.com":
        user = User(
            id="user123",
            email="user@example.com",
            hashed_password=get_password_hash("password"),
            full_name="John Doe",
            is_active=True,
            is_superuser=False,
            company_id="company123"
        )
    else:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user


async def get_current_company(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get the current user's company.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current company
    """
    # In a real implementation, this would query the database
    # For now, we'll just use a mock company
    
    # Mock company for development
    company = {
        "id": current_user.company_id,
        "name": "Acme Inc.",
        "industry": "Technology",
        "website": "https://example.com",
        "created_at": "2023-01-01T00:00:00Z"
    }
    
    return company

