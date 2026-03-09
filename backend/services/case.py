"""
Case management service.

This module provides case management functionality including:
- Creating new cases
- Retrieving cases with authorization checks
- Listing cases with role-based filtering
- Updating case status

Validates: Requirements FR2.1-FR2.5
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.case import Case
from models.user import User


class CaseService:
    """
    Case management service handling case operations.
    """
    
    @staticmethod
    def create_case(
        title: str,
        description: str,
        user_id: UUID,
        db: Session
    ) -> Case:
        """
        Create a new case filed by a citizen.
        
        Implements:
        - FR2.1: Citizens can file cases with title and description
        - FR2.2: Cases are assigned to the filing citizen
        - FR2.3: Cases start with FILED status
        
        Args:
            title: Case title (max 200 characters)
            description: Case description (max 10,000 characters)
            user_id: UUID of the citizen filing the case
            db: Database session
            
        Returns:
            Created Case object
            
        Raises:
            HTTPException 400: If validation fails
            HTTPException 404: If user not found
            
        Example:
            >>> case = CaseService.create_case(
            ...     title="Property Dispute",
            ...     description="Dispute over property ownership...",
            ...     user_id=UUID("..."),
            ...     db=db
            ... )
        """
        # Validate title length
        if not title or len(title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be between 1 and 200 characters"
            )
        
        # Validate description length
        if not description or len(description) > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be between 1 and 10,000 characters"
            )
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new case with FILED status (FR2.3)
        new_case = Case(
            title=title,
            description=description,
            user_id=user_id,
            status="FILED"
        )
        
        db.add(new_case)
        db.commit()
        db.refresh(new_case)
        
        return new_case
    
    @staticmethod
    def get_case_by_id(
        case_id: UUID,
        user_id: UUID,
        role: str,
        db: Session
    ) -> Case:
        """
        Get case details with authorization check.
        
        Implements:
        - FR2.4: Citizens can only view their own cases
        - FR2.5: Judges can view all cases
        
        Args:
            case_id: UUID of the case to retrieve
            user_id: UUID of the requesting user
            role: Role of the requesting user (CITIZEN or JUDGE)
            db: Database session
            
        Returns:
            Case object
            
        Raises:
            HTTPException 404: If case not found
            HTTPException 403: If citizen tries to access another's case
            
        Example:
            >>> case = CaseService.get_case_by_id(
            ...     case_id=UUID("..."),
            ...     user_id=UUID("..."),
            ...     role="CITIZEN",
            ...     db=db
            ... )
        """
        # Query case
        case = db.query(Case).filter(Case.id == case_id).first()
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Check authorization (FR2.4, FR2.5)
        if role == "CITIZEN" and case.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this case"
            )
        
        return case
    
    @staticmethod
    def list_cases(
        user_id: UUID,
        role: str,
        page: int = 1,
        limit: int = 10,
        db: Session = None
    ) -> tuple[List[Case], int]:
        """
        List cases with role-based filtering.
        
        Implements:
        - FR2.4: Citizens see only their own cases
        - FR2.5: Judges see all cases
        - Pagination support
        
        Args:
            user_id: UUID of the requesting user
            role: Role of the requesting user (CITIZEN or JUDGE)
            page: Page number (1-indexed)
            limit: Number of cases per page
            db: Database session
            
        Returns:
            Tuple of (list of Case objects, total count)
            
        Example:
            >>> cases, total = CaseService.list_cases(
            ...     user_id=UUID("..."),
            ...     role="CITIZEN",
            ...     page=1,
            ...     limit=10,
            ...     db=db
            ... )
        """
        # Build query based on role (FR2.4, FR2.5)
        if role == "CITIZEN":
            # Citizens see only their own cases
            query = db.query(Case).filter(Case.user_id == user_id)
        else:
            # Judges see all cases
            query = db.query(Case)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        cases = query.offset(offset).limit(limit).all()
        
        return cases, total
    
    @staticmethod
    def update_case_status(
        case_id: UUID,
        new_status: str,
        user_id: UUID,
        role: str,
        db: Session
    ) -> Case:
        """
        Update case status (judges only).
        
        Implements:
        - FR2.5: Judges can update case status
        - Valid statuses: FILED, IN_REVIEW, HEARING_SCHEDULED
        
        Args:
            case_id: UUID of the case to update
            new_status: New status value
            user_id: UUID of the requesting user
            role: Role of the requesting user
            db: Database session
            
        Returns:
            Updated Case object
            
        Raises:
            HTTPException 403: If not a judge
            HTTPException 404: If case not found
            HTTPException 400: If invalid status
            
        Example:
            >>> case = CaseService.update_case_status(
            ...     case_id=UUID("..."),
            ...     new_status="IN_REVIEW",
            ...     user_id=UUID("..."),
            ...     role="JUDGE",
            ...     db=db
            ... )
        """
        # Check authorization - only judges can update status
        if role != "JUDGE":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only judges can update case status"
            )
        
        # Validate status
        valid_statuses = ["FILED", "IN_REVIEW", "HEARING_SCHEDULED"]
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Query case
        case = db.query(Case).filter(Case.id == case_id).first()
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Update status
        case.status = new_status
        db.commit()
        db.refresh(case)
        
        return case
