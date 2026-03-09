"""
Authentication API endpoints.

Implements:
- POST /api/auth/register: User registration
- POST /api/auth/login: User login

Validates: Requirements FR1.1-FR1.10
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from services.auth import AuthService, UserCreate, UserLogin, TokenResponse


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Register a new user.
    
    Implements:
    - FR1.1: User registration with email, password, and role
    - FR1.2: Password hashing using bcrypt
    - FR1.3: Email format validation and uniqueness
    - FR1.4: Password length validation (min 8 characters)
    - FR1.5: JWT token generation upon successful registration
    - FR1.10: HTTP 400 for duplicate email
    
    Args:
        user_data: User registration data (email, password, role)
        db: Database session
        
    Returns:
        TokenResponse with access token, user_id, and role
        
    Raises:
        HTTPException 400: If email already exists or validation fails
        HTTPException 422: If request data is invalid
        
    Example:
        POST /api/auth/register
        {
            "email": "citizen@example.com",
            "password": "securepass123",
            "role": "CITIZEN"
        }
        
        Response (201):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "role": "CITIZEN"
        }
    """
    return AuthService.register_user(user_data, db)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> TokenResponse:
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
        HTTPException 401: If credentials are invalid
        HTTPException 422: If request data is invalid
        
    Example:
        POST /api/auth/login
        {
            "email": "citizen@example.com",
            "password": "securepass123"
        }
        
        Response (200):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "role": "CITIZEN"
        }
    """
    return AuthService.login_user(credentials, db)
