"""
Authentication service for user registration and login.

This module provides authentication functionality including:
- User registration with email validation and password hashing
- User login with credential verification and JWT token generation
- Email uniqueness validation
- Password length validation (min 8 characters)

Validates: Requirements FR1.1-FR1.10
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.user import User
from services.password import hash_password, verify_password
from services.jwt import create_access_token


class UserCreate(BaseModel):
    """
    Request model for user registration.
    
    Validates:
    - FR1.1: Email, password, and role required
    - FR1.3: Email format validation using Pydantic EmailStr
    - FR1.4: Password minimum 8 characters
    """
    email: EmailStr
    password: str
    role: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Validate password is at least 8 characters (FR1.4)."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is either CITIZEN or JUDGE."""
        if v not in ['CITIZEN', 'JUDGE']:
            raise ValueError('Role must be either CITIZEN or JUDGE')
        return v


class UserLogin(BaseModel):
    """
    Request model for user login.
    
    Validates:
    - FR1.6: Email and password required for login
    - Email format validation using Pydantic EmailStr
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Response model for authentication endpoints.
    
    Returns:
    - FR1.5: JWT token upon successful registration
    - FR1.7: JWT token with user_id and role claims upon successful login
    """
    access_token: str
    token_type: str
    user_id: UUID
    role: str


class AuthService:
    """
    Authentication service handling user registration and login.
    """
    
    @staticmethod
    def register_user(user_data: UserCreate, db: Session) -> TokenResponse:
        """
        Register a new user and return JWT token.
        
        Implements:
        - FR1.1: User registration with email, password, and role
        - FR1.2: Password hashing using bcrypt
        - FR1.3: Email format validation and uniqueness
        - FR1.4: Password length validation (min 8 characters)
        - FR1.5: JWT token generation upon successful registration
        
        Args:
            user_data: User registration data (email, password, role)
            db: Database session
            
        Returns:
            TokenResponse with access token, user_id, and role
            
        Raises:
            HTTPException 400: If email already exists (FR1.10)
            HTTPException 400: If validation fails
            
        Example:
            >>> user_data = UserCreate(
            ...     email="citizen@example.com",
            ...     password="securepass123",
            ...     role="CITIZEN"
            ... )
            >>> response = AuthService.register_user(user_data, db)
            >>> print(response.access_token)
        """
        # Hash password before storing (FR1.2, NFR2.1)
        password_hash = hash_password(user_data.password)
        
        # Create new user record
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            role=user_data.role
        )
        
        try:
            # Add user to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            # Email already exists (FR1.10)
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Generate JWT token (FR1.5, FR1.8)
        access_token = create_access_token(
            user_id=new_user.id,
            role=new_user.role
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            role=new_user.role
        )
    
    @staticmethod
    def login_user(credentials: UserLogin, db: Session) -> TokenResponse:
        """
        Authenticate user and return JWT token.
        
        Implements:
        - FR1.6: User login with email and password
        - FR1.7: JWT token with user_id and role claims
        - FR1.8: JWT token expiration (24 hours)
        - FR1.9: HTTP 401 for invalid credentials
        
        Args:
            credentials: User login credentials (email, password)
            db: Database session
            
        Returns:
            TokenResponse with access token, user_id, and role
            
        Raises:
            HTTPException 401: If credentials are invalid (FR1.9)
            
        Example:
            >>> credentials = UserLogin(
            ...     email="citizen@example.com",
            ...     password="securepass123"
            ... )
            >>> response = AuthService.login_user(credentials, db)
            >>> print(response.access_token)
        """
        # Query user by email
        user = db.query(User).filter(User.email == credentials.email).first()
        
        # Check if user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate JWT token (FR1.7, FR1.8)
        access_token = create_access_token(
            user_id=user.id,
            role=user.role
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            role=user.role
        )
