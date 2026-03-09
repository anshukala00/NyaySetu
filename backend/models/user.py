"""
User model for Nyaysetu Case Management System.

This module defines the User SQLAlchemy model with fields:
- id (UUID): Primary key
- email (String): Unique, indexed email address
- password_hash (String): Bcrypt hashed password
- role (String): User role ('CITIZEN' or 'JUDGE')

Validates: Requirements DR1.1, DR1.2, DR1.3
"""

import uuid
from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    User model representing citizens and judges in the system.
    
    Validation Rules (DR1):
    - email must be valid email format and unique
    - password must be at least 8 characters (hashed before storage)
    - role must be either 'CITIZEN' or 'JUDGE'
    
    Note: Relationships to Case model will be added in task 2.1.4
    """
    __tablename__ = "users"
    
    # Primary key: UUID v4 auto-generated (DR1.4)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Email: unique, non-null, indexed for fast login queries (DR1.2, NFR3.1)
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Password hash: bcrypt hashed password, never store plaintext (NFR2.1)
    password_hash = Column(String, nullable=False)
    
    # Role: 'CITIZEN' or 'JUDGE' (DR1.3)
    role = Column(String, nullable=False)
    
    # Relationships to Case model (Task 2.1.4)
    # filed_cases: Cases filed by this user (when role='CITIZEN')
    # assigned_cases: Cases assigned to this user (when role='JUDGE')
    filed_cases = relationship(
        "Case", 
        foreign_keys="Case.user_id", 
        back_populates="citizen"
    )
    assigned_cases = relationship(
        "Case", 
        foreign_keys="Case.judge_id", 
        back_populates="judge"
    )
    
    def __repr__(self):
        """String representation of User model."""
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
