"""
AI services API endpoints.

Implements:
- POST /api/triage/{case_id}: Triage a case
- POST /api/ai/summarize/{case_id}: Generate case summary
- GET /api/precedents/search: Search for precedents

Validates: Requirements FR3.1-FR3.7
"""

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from services.jwt import get_current_user
from services.ai import AIService


# Pydantic models
class TriageResponse(BaseModel):
    """Response model for case triage."""
    case_id: UUID
    priority: str
    message: str


class SummaryResponse(BaseModel):
    """Response model for case summary."""
    case_id: UUID
    ai_summary: str
    message: str


class PrecedentResult(BaseModel):
    """Response model for a single precedent."""
    id: str
    title: str
    summary: str
    relevance_score: int


class PrecedentSearchResponse(BaseModel):
    """Response model for precedent search results."""
    query: str
    results: List[PrecedentResult]
    total: int


router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/triage/{case_id}", response_model=TriageResponse)
async def triage_case(
    case_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TriageResponse:
    """
    Triage a case using AI keyword detection.
    
    Implements:
    - FR3.1: Triage cases based on keywords
    - FR3.2: Set priority to HIGH for urgent cases
    - FR3.3: Set priority to REGULAR for non-urgent cases
    
    Args:
        case_id: UUID of the case to triage
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Triage result with priority level
        
    Raises:
        HTTPException 404: If case not found
        
    Example:
        POST /api/triage/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer <token>
        
        Response (200):
        {
            "case_id": "550e8400-e29b-41d4-a716-446655440000",
            "priority": "HIGH",
            "message": "Case triaged successfully"
        }
    """
    # Get case to verify it exists and get description
    from services.case import CaseService
    
    try:
        case = CaseService.get_case_by_id(
            case_id=case_id,
            user_id=current_user["user_id"],
            role=current_user["role"],
            db=db
        )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Triage the case
    triaged_case = AIService.triage_case(case_id, case.description, db)
    
    if not triaged_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    return TriageResponse(
        case_id=triaged_case.id,
        priority=triaged_case.priority,
        message="Case triaged successfully"
    )


@router.post("/ai/summarize/{case_id}", response_model=SummaryResponse)
async def summarize_case(
    case_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> SummaryResponse:
    """
    Generate an AI summary for a case.
    
    Implements:
    - FR3.4: Generate case summaries
    - FR3.5: Append "[AI Generated Summary]" suffix
    
    Args:
        case_id: UUID of the case to summarize
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Summary result with generated summary text
        
    Raises:
        HTTPException 404: If case not found
        
    Example:
        POST /api/ai/summarize/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer <token>
        
        Response (200):
        {
            "case_id": "550e8400-e29b-41d4-a716-446655440000",
            "ai_summary": "This is a case about property dispute...",
            "message": "Summary generated successfully"
        }
    """
    # Get case to verify it exists and get description
    from services.case import CaseService
    
    try:
        case = CaseService.get_case_by_id(
            case_id=case_id,
            user_id=current_user["user_id"],
            role=current_user["role"],
            db=db
        )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Generate summary
    summarized_case = AIService.generate_summary(case_id, case.description, db)
    
    if not summarized_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    return SummaryResponse(
        case_id=summarized_case.id,
        ai_summary=summarized_case.ai_summary,
        message="Summary generated successfully"
    )


@router.get("/precedents/search", response_model=PrecedentSearchResponse)
async def search_precedents(
    q: str = Query(..., min_length=1, description="Search query"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PrecedentSearchResponse:
    """
    Search for relevant legal precedents.
    
    Implements:
    - FR3.6: Search precedents by keywords
    - FR3.7: Return results ranked by relevance
    
    Args:
        q: Search query string
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of precedents ranked by relevance
        
    Example:
        GET /api/precedents/search?q=property%20dispute
        Authorization: Bearer <token>
        
        Response (200):
        {
            "query": "property dispute",
            "results": [
                {
                    "id": "prec-001",
                    "title": "Property Boundary Dispute Resolution",
                    "summary": "Established legal precedent...",
                    "relevance_score": 5
                }
            ],
            "total": 3
        }
    """
    # Search precedents
    results = AIService.search_precedents(q)
    
    # Convert to response models
    precedent_results = [
        PrecedentResult(
            id=result["id"],
            title=result["title"],
            summary=result["summary"],
            relevance_score=result["relevance_score"]
        )
        for result in results
    ]
    
    return PrecedentSearchResponse(
        query=q,
        results=precedent_results,
        total=len(precedent_results)
    )
