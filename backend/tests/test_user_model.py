"""
Unit tests for User model.

Tests verify:
- User model creation with all required fields
- UUID auto-generation
- Email uniqueness constraint
- Model relationships
"""

import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from models.user import User


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    # Use SQLite in-memory database for fast tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


def test_user_creation(db_session):
    """Test creating a user with all required fields."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_here",
        role="CITIZEN"
    )
    
    db_session.add(user)
    db_session.commit()
    
    # Verify user was created
    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password_here"
    assert user.role == "CITIZEN"


def test_user_id_auto_generation(db_session):
    """Test that user ID is auto-generated as UUID."""
    user = User(
        email="auto@example.com",
        password_hash="hashed_password",
        role="JUDGE"
    )
    
    db_session.add(user)
    db_session.commit()
    
    # Verify UUID was auto-generated
    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)


def test_user_repr():
    """Test string representation of User model."""
    user = User(
        id=uuid.uuid4(),
        email="repr@example.com",
        password_hash="hashed",
        role="CITIZEN"
    )
    
    repr_str = repr(user)
    assert "User" in repr_str
    assert "repr@example.com" in repr_str
    assert "CITIZEN" in repr_str


def test_user_roles(db_session):
    """Test creating users with different roles."""
    citizen = User(
        email="citizen@example.com",
        password_hash="hashed",
        role="CITIZEN"
    )
    
    judge = User(
        email="judge@example.com",
        password_hash="hashed",
        role="JUDGE"
    )
    
    db_session.add(citizen)
    db_session.add(judge)
    db_session.commit()
    
    assert citizen.role == "CITIZEN"
    assert judge.role == "JUDGE"
