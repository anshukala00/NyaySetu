"""
Case model for Nyaysetu Case Management System.

This module defines the Case SQLAlchemy model with fields:
- id (UUID): Primary key
- title (String): Case title (max 200 characters)
- description (Text): Case description
- status (String): Case status ('FILED', 'IN_REVIEW', 'HEARING_SCHEDULED')
- user_id (UUID): Foreign key to users table (citizen who filed the case)
- judge_id (UUID): Foreign key to users table (assigned judge, nullable)
- priority (String): Case priority ('HIGH' or 'REGULAR', nullable)
- ai_summary (Text): AI-generated summary (nullable)
- created_at (DateTime): Case creation timestamp

Validates: Requirements DR2.1, DR2.2, DR2.3, DR2.4, DR2.5, DR2.6, DR2.7
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Case(Base):
    """
    Case model representing legal cases filed by citizens.
    
    Validation Rules (DR2):
    - title must be non-empty string (max 200 characters)
    - description must be non-empty text
    - status must be one of: 'FILED', 'IN_REVIEW', 'HEARING_SCHEDULED'
    - user_id must reference valid user with role='CITIZEN'
    - judge_id must reference valid user with role='JUDGE' (if not null)
    - priority must be 'HIGH' or 'REGULAR' (if not null)
    """
    __tablename__ = "cases"
    
    # Primary key: UUID v4 auto-generated (DR2.6)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Title: non-empty string, max 200 characters (DR2.1, NFR2.8)
    title = Column(String(200), nullable=False)
    
    # Description: non-empty text, max 10,000 characters (DR2.1, NFR2.9)
    description = Column(Text, nullable=False)
    
    # Status: one of 'FILED', 'IN_REVIEW', 'HEARING_SCHEDULED' (DR2.2)
    # Default to 'FILED' when case is created (FR2.3)
    status = Column(String, nullable=False, default='FILED')
    
    # Foreign key to users table: citizen who filed the case (DR2.4)
    # Indexed for fast case retrieval by citizen (NFR6.3, Task 2.2.3)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('users.id'), 
        nullable=False,
        index=True
    )
    
    # Foreign key to users table: assigned judge (DR2.5)
    # Nullable because cases may not have assigned judge initially
    judge_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('users.id'), 
        nullable=True
    )
    
    # Priority: 'HIGH' or 'REGULAR', assigned by AI triage (DR2.3)
    priority = Column(String, nullable=True)
    
    # AI-generated summary (FR4.3)
    ai_summary = Column(Text, nullable=True)
    
    # Creation timestamp: defaults to current UTC time (DR2.7)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships to User model (Task 2.2.4)
    # citizen: The user who filed this case (role='CITIZEN')
    # judge: The judge assigned to this case (role='JUDGE')
    citizen = relationship(
        "User", 
        foreign_keys=[user_id], 
        back_populates="filed_cases"
    )
    judge = relationship(
        "User", 
        foreign_keys=[judge_id], 
        back_populates="assigned_cases"
    )
    
    def __repr__(self):
        """String representation of Case model."""
        return f"<Case(id={self.id}, title={self.title}, status={self.status}, priority={self.priority})>"


# Additional index on status field for filtering (NFR6.3, Task 2.2.3)
Index('ix_cases_status', Case.status)
