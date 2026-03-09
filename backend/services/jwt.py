"""
JWT token generation and verification service.

This module provides JWT token handling for authentication as per FR1.7 and FR1.8.
Uses python-jose library for JWT operations with HS256 algorithm.
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration from environment variables
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Validate JWT_SECRET is set
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable must be set")

# Security scheme for FastAPI
security = HTTPBearer()


def create_access_token(user_id: UUID, role: str) -> str:
    """
    Generate JWT access token with user_id and role claims.
    
    Token expires in 24 hours as per FR1.8.
    
    Args:
        user_id: User's UUID
        role: User's role (CITIZEN or JUDGE)
        
    Returns:
        JWT token string
        
    Raises:
        ValueError: If user_id or role is invalid
        
    Example:
        >>> token = create_access_token(user_id=UUID("..."), role="CITIZEN")
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    if not user_id:
        raise ValueError("user_id cannot be None")
    if role not in ["CITIZEN", "JUDGE"]:
        raise ValueError("role must be either 'CITIZEN' or 'JUDGE'")
    
    # Calculate expiration time (24 hours from now)
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    # Create token payload with claims
    payload = {
        "sub": str(user_id),  # Subject: user_id
        "role": role,          # Custom claim: user role
        "exp": expire,         # Expiration time
        "iat": datetime.utcnow()  # Issued at time
    }
    
    # Generate and return JWT token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Decoded token payload containing user_id and role
        
    Raises:
        HTTPException: If token is invalid or expired (401)
        
    Example:
        >>> payload = verify_token(token)
        >>> print(payload["sub"])  # user_id
        >>> print(payload["role"])  # role
    """
    try:
        # Decode and verify token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        # Token is invalid or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency to extract and verify current user from JWT token.
    
    This function is used as a dependency in protected endpoints to automatically
    extract and validate the JWT token from the Authorization header.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        
    Returns:
        Dictionary containing user_id and role:
        {
            "user_id": UUID,
            "role": str
        }
        
    Raises:
        HTTPException: If token is missing, invalid, or expired (401)
        
    Example:
        @app.get("/api/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            user_id = current_user["user_id"]
            role = current_user["role"]
            return {"message": f"Hello {role}"}
    """
    # Extract token from credentials
    token = credentials.credentials
    
    # Verify token and get payload
    payload = verify_token(token)
    
    # Extract user_id and role from payload
    user_id_str = payload.get("sub")
    role = payload.get("role")
    
    if not user_id_str or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert user_id string back to UUID
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user_id,
        "role": role
    }
