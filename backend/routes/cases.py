"""
Case management API endpoints.

Implements:
- POST /api/cases: Create a new case (citizen only)
- GET /api/cases: List cases (role-based filtering)
- GET /api/cases/{id}: Get case details (with authorization)
- PATCH /api/cases/{id}/status: Update case status (judge only)

Validates: Requirements FR2.1-FR2.5
"""

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from services.jwt import get_current_user
from services.case import CaseService
from services.ai import AIService


# Pydantic models
class CaseCreate(BaseModel):
    """Request model for creating a case."""
    title: str = Field(..., min_length=1, max_length=200, description="Case title")
    description: str = Field(..., min_length=1, max_length=10000, description="Case description")


class CaseUpdate(BaseModel):
    """Request model for updating case status."""
    status: str = Field(..., description="New case status")


class CaseResponse(BaseModel):
    """Response model for case details."""
    id: UUID
    title: str
    description: str
    status: str
    user_id: UUID
    judge_id: UUID | None = None
    priority: str | None = None
    ai_summary: str | None = None
    created_at: str | None = None
    
    model_config = {"from_attributes": True}


class CaseListResponse(BaseModel):
    """Response model for case list."""
    cases: List[CaseResponse]
    total: int
    page: int
    limit: int


router = APIRouter(prefix="/api/cases", tags=["cases"])


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CaseResponse:
    """
    Create a new case (citizen only).
    
    Implements:
    - FR2.1: Citizens can file cases with title and description
    - FR2.2: Cases are assigned to the filing citizen
    - FR2.3: Cases start with FILED status
    
    Args:
        case_data: Case creation data (title, description)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created case details
        
    Raises:
        HTTPException 403: If not a citizen
        HTTPException 400: If validation fails
        
    Example:
        POST /api/cases
        Authorization: Bearer <token>
        {
            "title": "Property Dispute",
            "description": "Dispute over property ownership..."
        }
        
        Response (201):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Property Dispute",
            "description": "Dispute over property ownership...",
            "status": "FILED",
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            "judge_id": null,
            "priority": null,
            "ai_summary": null,
            "created_at": "2024-01-15T10:30:00"
        }
    """
    # Check authorization - only citizens can create cases
    if current_user["role"] != "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only citizens can file cases"
        )
    
    # Create case
    case = CaseService.create_case(
        title=case_data.title,
        description=case_data.description,
        user_id=current_user["user_id"],
        db=db
    )
    
    # Automatically trigger AI triage (FR2.4)
    try:
        AIService.triage_case(case.id, case.description, db)
        # Refresh case to get updated priority
        db.refresh(case)
    except Exception as e:
        # Log error but don't fail the case creation
        print(f"Warning: AI triage failed for case {case.id}: {str(e)}")
    
    # Convert to response model with datetime conversion
    case_dict = {
        "id": case.id,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "user_id": case.user_id,
        "judge_id": case.judge_id,
        "priority": case.priority,
        "ai_summary": case.ai_summary,
        "created_at": case.created_at.isoformat() if case.created_at else None
    }
    return CaseResponse(**case_dict)


@router.get("", response_model=CaseListResponse)
async def list_cases(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CaseListResponse:
    """
    List cases with role-based filtering.
    
    Implements:
    - FR2.4: Citizens see only their own cases
    - FR2.5: Judges see all cases
    - Pagination support
    
    Args:
        page: Page number (1-indexed)
        limit: Number of cases per page
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of cases with pagination info
        
    Example:
        GET /api/cases?page=1&limit=10
        Authorization: Bearer <token>
        
        Response (200):
        {
            "cases": [...],
            "total": 25,
            "page": 1,
            "limit": 10
        }
    """
    cases, total = CaseService.list_cases(
        user_id=current_user["user_id"],
        role=current_user["role"],
        page=page,
        limit=limit,
        db=db
    )
    
    case_responses = []
    for case in cases:
        case_dict = {
            "id": case.id,
            "title": case.title,
            "description": case.description,
            "status": case.status,
            "user_id": case.user_id,
            "judge_id": case.judge_id,
            "priority": case.priority,
            "ai_summary": case.ai_summary,
            "created_at": case.created_at.isoformat() if case.created_at else None
        }
        case_responses.append(CaseResponse(**case_dict))
    
    return CaseListResponse(
        cases=case_responses,
        total=total,
        page=page,
        limit=limit
    )


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CaseResponse:
    """
    Get case details with authorization check.
    
    Implements:
    - FR2.4: Citizens can only view their own cases
    - FR2.5: Judges can view all cases
    
    Args:
        case_id: UUID of the case to retrieve
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Case details
        
    Raises:
        HTTPException 404: If case not found
        HTTPException 403: If citizen tries to access another's case
        
    Example:
        GET /api/cases/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer <token>
        
        Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Property Dispute",
            "description": "Dispute over property ownership...",
            "status": "FILED",
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            ...
        }
    """
    case = CaseService.get_case_by_id(
        case_id=case_id,
        user_id=current_user["user_id"],
        role=current_user["role"],
        db=db
    )
    
    case_dict = {
        "id": case.id,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "user_id": case.user_id,
        "judge_id": case.judge_id,
        "priority": case.priority,
        "ai_summary": case.ai_summary,
        "created_at": case.created_at.isoformat() if case.created_at else None
    }
    return CaseResponse(**case_dict)


@router.patch("/{case_id}/status", response_model=CaseResponse)
async def update_case_status(
    case_id: UUID,
    status_update: CaseUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CaseResponse:
    """
    Update case status (judge only).
    
    Implements:
    - FR2.5: Judges can update case status
    - Valid statuses: FILED, IN_REVIEW, HEARING_SCHEDULED
    
    Args:
        case_id: UUID of the case to update
        status_update: New status value
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated case details
        
    Raises:
        HTTPException 403: If not a judge
        HTTPException 404: If case not found
        HTTPException 400: If invalid status
        
    Example:
        PATCH /api/cases/550e8400-e29b-41d4-a716-446655440000/status
        Authorization: Bearer <token>
        {
            "status": "IN_REVIEW"
        }
        
        Response (200):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Property Dispute",
            "description": "Dispute over property ownership...",
            "status": "IN_REVIEW",
            ...
        }
    """
    case = CaseService.update_case_status(
        case_id=case_id,
        new_status=status_update.status,
        user_id=current_user["user_id"],
        role=current_user["role"],
        db=db
    )
    
    case_dict = {
        "id": case.id,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "user_id": case.user_id,
        "judge_id": case.judge_id,
        "priority": case.priority,
        "ai_summary": case.ai_summary,
        "created_at": case.created_at.isoformat() if case.created_at else None
    }
    return CaseResponse(**case_dict)
