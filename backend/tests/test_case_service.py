"""
Unit tests for case management service.

Tests cover:
- Creating cases
- Retrieving cases with authorization
- Listing cases with role-based filtering
- Updating case status
- Error handling
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from models.user import User
from models.case import Case
from app.database import Base
from services.case import CaseService
from services.password import hash_password


# Create in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def citizen_user(test_db: Session):
    """Create a test citizen user."""
    user = User(
        email="citizen@example.com",
        password_hash=hash_password("password123"),
        role="CITIZEN"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def judge_user(test_db: Session):
    """Create a test judge user."""
    user = User(
        email="judge@example.com",
        password_hash=hash_password("password123"),
        role="JUDGE"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


class TestCreateCase:
    """Test case creation functionality."""
    
    def test_create_case_with_valid_data(self, test_db: Session, citizen_user: User):
        """Test successful case creation."""
        case = CaseService.create_case(
            title="Property Dispute",
            description="Dispute over property ownership between neighbors",
            user_id=citizen_user.id,
            db=test_db
        )
        
        assert case.id is not None
        assert case.title == "Property Dispute"
        assert case.description == "Dispute over property ownership between neighbors"
        assert case.user_id == citizen_user.id
        assert case.status == "FILED"
    
    def test_create_case_stores_in_database(self, test_db: Session, citizen_user: User):
        """Test that created case is stored in database."""
        case = CaseService.create_case(
            title="Contract Dispute",
            description="Breach of contract claim",
            user_id=citizen_user.id,
            db=test_db
        )
        
        # Query database to verify
        stored_case = test_db.query(Case).filter(Case.id == case.id).first()
        
        assert stored_case is not None
        assert stored_case.title == "Contract Dispute"
    
    def test_create_case_with_empty_title_raises_error(self, test_db: Session, citizen_user: User):
        """Test that empty title raises error."""
        with pytest.raises(Exception) as exc_info:
            CaseService.create_case(
                title="",
                description="Valid description",
                user_id=citizen_user.id,
                db=test_db
            )
        
        assert "Title must be between" in str(exc_info.value)
    
    def test_create_case_with_title_too_long_raises_error(self, test_db: Session, citizen_user: User):
        """Test that title longer than 200 characters raises error."""
        long_title = "a" * 201
        
        with pytest.raises(Exception) as exc_info:
            CaseService.create_case(
                title=long_title,
                description="Valid description",
                user_id=citizen_user.id,
                db=test_db
            )
        
        assert "Title must be between" in str(exc_info.value)
    
    def test_create_case_with_empty_description_raises_error(self, test_db: Session, citizen_user: User):
        """Test that empty description raises error."""
        with pytest.raises(Exception) as exc_info:
            CaseService.create_case(
                title="Valid Title",
                description="",
                user_id=citizen_user.id,
                db=test_db
            )
        
        assert "Description must be between" in str(exc_info.value)
    
    def test_create_case_with_description_too_long_raises_error(self, test_db: Session, citizen_user: User):
        """Test that description longer than 10,000 characters raises error."""
        long_description = "a" * 10001
        
        with pytest.raises(Exception) as exc_info:
            CaseService.create_case(
                title="Valid Title",
                description=long_description,
                user_id=citizen_user.id,
                db=test_db
            )
        
        assert "Description must be between" in str(exc_info.value)
    
    def test_create_case_with_nonexistent_user_raises_error(self, test_db: Session):
        """Test that creating case with non-existent user raises error."""
        fake_user_id = uuid4()
        
        with pytest.raises(Exception) as exc_info:
            CaseService.create_case(
                title="Valid Title",
                description="Valid description",
                user_id=fake_user_id,
                db=test_db
            )
        
        assert "User not found" in str(exc_info.value)


class TestGetCaseById:
    """Test case retrieval with authorization."""
    
    def test_citizen_can_view_own_case(self, test_db: Session, citizen_user: User):
        """Test that citizen can view their own case."""
        case = CaseService.create_case(
            title="My Case",
            description="My case description",
            user_id=citizen_user.id,
            db=test_db
        )
        
        retrieved_case = CaseService.get_case_by_id(
            case_id=case.id,
            user_id=citizen_user.id,
            role="CITIZEN",
            db=test_db
        )
        
        assert retrieved_case.id == case.id
    
    def test_citizen_cannot_view_other_citizen_case(self, test_db: Session, citizen_user: User):
        """Test that citizen cannot view another citizen's case."""
        # Create another citizen
        other_citizen = User(
            email="other@example.com",
            password_hash=hash_password("password123"),
            role="CITIZEN"
        )
        test_db.add(other_citizen)
        test_db.commit()
        test_db.refresh(other_citizen)
        
        # Create case for first citizen
        case = CaseService.create_case(
            title="Other's Case",
            description="Another citizen's case",
            user_id=other_citizen.id,
            db=test_db
        )
        
        # Try to access as first citizen
        with pytest.raises(Exception) as exc_info:
            CaseService.get_case_by_id(
                case_id=case.id,
                user_id=citizen_user.id,
                role="CITIZEN",
                db=test_db
            )
        
        assert "permission" in str(exc_info.value).lower()
    
    def test_judge_can_view_any_case(self, test_db: Session, citizen_user: User, judge_user: User):
        """Test that judge can view any case."""
        case = CaseService.create_case(
            title="Any Case",
            description="Case for judge to view",
            user_id=citizen_user.id,
            db=test_db
        )
        
        retrieved_case = CaseService.get_case_by_id(
            case_id=case.id,
            user_id=judge_user.id,
            role="JUDGE",
            db=test_db
        )
        
        assert retrieved_case.id == case.id
    
    def test_get_nonexistent_case_raises_error(self, test_db: Session, citizen_user: User):
        """Test that getting non-existent case raises error."""
        fake_case_id = uuid4()
        
        with pytest.raises(Exception) as exc_info:
            CaseService.get_case_by_id(
                case_id=fake_case_id,
                user_id=citizen_user.id,
                role="CITIZEN",
                db=test_db
            )
        
        assert "Case not found" in str(exc_info.value)


class TestListCases:
    """Test case listing with role-based filtering."""
    
    def test_citizen_sees_only_own_cases(self, test_db: Session, citizen_user: User):
        """Test that citizen sees only their own cases."""
        # Create another citizen
        other_citizen = User(
            email="other@example.com",
            password_hash=hash_password("password123"),
            role="CITIZEN"
        )
        test_db.add(other_citizen)
        test_db.commit()
        test_db.refresh(other_citizen)
        
        # Create cases for both citizens
        case1 = CaseService.create_case(
            title="Case 1",
            description="First citizen's case",
            user_id=citizen_user.id,
            db=test_db
        )
        case2 = CaseService.create_case(
            title="Case 2",
            description="Other citizen's case",
            user_id=other_citizen.id,
            db=test_db
        )
        
        # List cases as first citizen
        cases, total = CaseService.list_cases(
            user_id=citizen_user.id,
            role="CITIZEN",
            db=test_db
        )
        
        assert len(cases) == 1
        assert cases[0].id == case1.id
        assert total == 1
    
    def test_judge_sees_all_cases(self, test_db: Session, citizen_user: User, judge_user: User):
        """Test that judge sees all cases."""
        # Create another citizen
        other_citizen = User(
            email="other@example.com",
            password_hash=hash_password("password123"),
            role="CITIZEN"
        )
        test_db.add(other_citizen)
        test_db.commit()
        test_db.refresh(other_citizen)
        
        # Create cases for both citizens
        case1 = CaseService.create_case(
            title="Case 1",
            description="First citizen's case",
            user_id=citizen_user.id,
            db=test_db
        )
        case2 = CaseService.create_case(
            title="Case 2",
            description="Other citizen's case",
            user_id=other_citizen.id,
            db=test_db
        )
        
        # List cases as judge
        cases, total = CaseService.list_cases(
            user_id=judge_user.id,
            role="JUDGE",
            db=test_db
        )
        
        assert len(cases) == 2
        assert total == 2
    
    def test_list_cases_pagination(self, test_db: Session, citizen_user: User):
        """Test pagination in case listing."""
        # Create 15 cases
        for i in range(15):
            CaseService.create_case(
                title=f"Case {i+1}",
                description=f"Case {i+1} description",
                user_id=citizen_user.id,
                db=test_db
            )
        
        # Get first page (10 items)
        cases_page1, total = CaseService.list_cases(
            user_id=citizen_user.id,
            role="CITIZEN",
            page=1,
            limit=10,
            db=test_db
        )
        
        # Get second page (5 items)
        cases_page2, _ = CaseService.list_cases(
            user_id=citizen_user.id,
            role="CITIZEN",
            page=2,
            limit=10,
            db=test_db
        )
        
        assert len(cases_page1) == 10
        assert len(cases_page2) == 5
        assert total == 15


class TestUpdateCaseStatus:
    """Test case status updates."""
    
    def test_judge_can_update_case_status(self, test_db: Session, citizen_user: User, judge_user: User):
        """Test that judge can update case status."""
        case = CaseService.create_case(
            title="Case to Update",
            description="Case for status update",
            user_id=citizen_user.id,
            db=test_db
        )
        
        updated_case = CaseService.update_case_status(
            case_id=case.id,
            new_status="IN_REVIEW",
            user_id=judge_user.id,
            role="JUDGE",
            db=test_db
        )
        
        assert updated_case.status == "IN_REVIEW"
    
    def test_citizen_cannot_update_case_status(self, test_db: Session, citizen_user: User):
        """Test that citizen cannot update case status."""
        case = CaseService.create_case(
            title="Case to Update",
            description="Case for status update",
            user_id=citizen_user.id,
            db=test_db
        )
        
        with pytest.raises(Exception) as exc_info:
            CaseService.update_case_status(
                case_id=case.id,
                new_status="IN_REVIEW",
                user_id=citizen_user.id,
                role="CITIZEN",
                db=test_db
            )
        
        assert "Only judges" in str(exc_info.value)
    
    def test_update_case_with_invalid_status_raises_error(self, test_db: Session, citizen_user: User, judge_user: User):
        """Test that invalid status raises error."""
        case = CaseService.create_case(
            title="Case to Update",
            description="Case for status update",
            user_id=citizen_user.id,
            db=test_db
        )
        
        with pytest.raises(Exception) as exc_info:
            CaseService.update_case_status(
                case_id=case.id,
                new_status="INVALID_STATUS",
                user_id=judge_user.id,
                role="JUDGE",
                db=test_db
            )
        
        assert "Invalid status" in str(exc_info.value)
    
    def test_update_nonexistent_case_raises_error(self, test_db: Session, judge_user: User):
        """Test that updating non-existent case raises error."""
        fake_case_id = uuid4()
        
        with pytest.raises(Exception) as exc_info:
            CaseService.update_case_status(
                case_id=fake_case_id,
                new_status="IN_REVIEW",
                user_id=judge_user.id,
                role="JUDGE",
                db=test_db
            )
        
        assert "Case not found" in str(exc_info.value)
    
    def test_update_case_through_all_statuses(self, test_db: Session, citizen_user: User, judge_user: User):
        """Test updating case through all valid statuses."""
        case = CaseService.create_case(
            title="Case Status Flow",
            description="Test case status transitions",
            user_id=citizen_user.id,
            db=test_db
        )
        
        # FILED -> IN_REVIEW
        case = CaseService.update_case_status(
            case_id=case.id,
            new_status="IN_REVIEW",
            user_id=judge_user.id,
            role="JUDGE",
            db=test_db
        )
        assert case.status == "IN_REVIEW"
        
        # IN_REVIEW -> HEARING_SCHEDULED
        case = CaseService.update_case_status(
            case_id=case.id,
            new_status="HEARING_SCHEDULED",
            user_id=judge_user.id,
            role="JUDGE",
            db=test_db
        )
        assert case.status == "HEARING_SCHEDULED"
