"""
Unit tests for AI services.

Tests cover:
- Case triage with keyword detection
- Case summary generation
- Precedent search with text matching
- Relevance scoring
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
from services.ai import AIService
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


class TestTriageCase:
    """Test case triage functionality."""
    
    def test_triage_urgent_case(self, test_db: Session, citizen_user: User):
        """Test that urgent keywords set priority to HIGH."""
        case = CaseService.create_case(
            title="Assault Case",
            description="I was assaulted by my neighbor yesterday",
            user_id=citizen_user.id,
            db=test_db
        )
        
        triaged_case = AIService.triage_case(case.id, case.description, test_db)
        
        assert triaged_case.priority == "HIGH"
    
    def test_triage_regular_case(self, test_db: Session, citizen_user: User):
        """Test that non-urgent cases set priority to REGULAR."""
        case = CaseService.create_case(
            title="Property Dispute",
            description="I have a dispute with my neighbor about property boundaries",
            user_id=citizen_user.id,
            db=test_db
        )
        
        triaged_case = AIService.triage_case(case.id, case.description, test_db)
        
        assert triaged_case.priority == "REGULAR"
    
    def test_triage_with_urgent_keyword(self, test_db: Session, citizen_user: User):
        """Test triage with various urgent keywords."""
        urgent_keywords = ["urgent", "assault", "emergency", "immediate", "critical", "violence", "injury"]
        
        for keyword in urgent_keywords:
            case = CaseService.create_case(
                title=f"Case with {keyword}",
                description=f"This is a {keyword} matter",
                user_id=citizen_user.id,
                db=test_db
            )
            
            triaged_case = AIService.triage_case(case.id, case.description, test_db)
            
            assert triaged_case.priority == "HIGH", f"Failed for keyword: {keyword}"
    
    def test_triage_case_insensitive(self, test_db: Session, citizen_user: User):
        """Test that triage is case-insensitive."""
        case = CaseService.create_case(
            title="Urgent Case",
            description="This is an URGENT matter that needs immediate attention",
            user_id=citizen_user.id,
            db=test_db
        )
        
        triaged_case = AIService.triage_case(case.id, case.description, test_db)
        
        assert triaged_case.priority == "HIGH"
    
    def test_triage_nonexistent_case_returns_none(self, test_db: Session):
        """Test that triaging non-existent case returns None."""
        fake_case_id = uuid4()
        
        result = AIService.triage_case(fake_case_id, "description", test_db)
        
        assert result is None


class TestGenerateSummary:
    """Test case summary generation."""
    
    def test_generate_summary_short_description(self, test_db: Session, citizen_user: User):
        """Test summary generation for short descriptions."""
        description = "This is a short case description"
        case = CaseService.create_case(
            title="Short Case",
            description=description,
            user_id=citizen_user.id,
            db=test_db
        )
        
        summarized_case = AIService.generate_summary(case.id, description, test_db)
        
        assert summarized_case.ai_summary == description + " [AI Generated Summary]"
    
    def test_generate_summary_long_description(self, test_db: Session, citizen_user: User):
        """Test summary generation for long descriptions (truncated to 200 chars)."""
        long_description = "a" * 300
        case = CaseService.create_case(
            title="Long Case",
            description=long_description,
            user_id=citizen_user.id,
            db=test_db
        )
        
        summarized_case = AIService.generate_summary(case.id, long_description, test_db)
        
        # Should be truncated to 200 chars + "..." + " [AI Generated Summary]"
        expected = "a" * 200 + "... [AI Generated Summary]"
        assert summarized_case.ai_summary == expected
    
    def test_generate_summary_exactly_200_chars(self, test_db: Session, citizen_user: User):
        """Test summary generation for exactly 200 character description."""
        description = "a" * 200
        case = CaseService.create_case(
            title="Exact Case",
            description=description,
            user_id=citizen_user.id,
            db=test_db
        )
        
        summarized_case = AIService.generate_summary(case.id, description, test_db)
        
        # Should not add "..." since it's exactly 200 chars
        expected = description + " [AI Generated Summary]"
        assert summarized_case.ai_summary == expected
    
    def test_generate_summary_appends_marker(self, test_db: Session, citizen_user: User):
        """Test that summary always appends AI marker."""
        description = "Property dispute case"
        case = CaseService.create_case(
            title="Property Case",
            description=description,
            user_id=citizen_user.id,
            db=test_db
        )
        
        summarized_case = AIService.generate_summary(case.id, description, test_db)
        
        assert "[AI Generated Summary]" in summarized_case.ai_summary
    
    def test_generate_summary_nonexistent_case_returns_none(self, test_db: Session):
        """Test that summarizing non-existent case returns None."""
        fake_case_id = uuid4()
        
        result = AIService.generate_summary(fake_case_id, "description", test_db)
        
        assert result is None


class TestSearchPrecedents:
    """Test precedent search functionality."""
    
    def test_search_precedents_single_keyword(self):
        """Test searching precedents with single keyword."""
        results = AIService.search_precedents("property")
        
        assert len(results) > 0
        # Property should match "Property Boundary Dispute Resolution"
        assert any("property" in r["title"].lower() for r in results)
    
    def test_search_precedents_multiple_keywords(self):
        """Test searching precedents with multiple keywords."""
        results = AIService.search_precedents("property dispute")
        
        assert len(results) > 0
        # Should find property-related precedents
        assert any("property" in r["title"].lower() for r in results)
    
    def test_search_precedents_returns_ranked_results(self):
        """Test that results are ranked by relevance."""
        results = AIService.search_precedents("property boundary")
        
        assert len(results) > 0
        # Results should be sorted by relevance_score (descending)
        for i in range(len(results) - 1):
            assert results[i]["relevance_score"] >= results[i + 1]["relevance_score"]
    
    def test_search_precedents_title_match_highest_score(self):
        """Test that title matches score higher than summary matches."""
        # "Property Boundary Dispute Resolution" has "property" in title
        results = AIService.search_precedents("property")
        
        assert len(results) > 0
        # First result should be the one with "property" in title
        assert "property" in results[0]["title"].lower()
    
    def test_search_precedents_no_matches(self):
        """Test searching with query that has no matches."""
        results = AIService.search_precedents("xyz123nonexistent")
        
        assert len(results) == 0
    
    def test_search_precedents_case_insensitive(self):
        """Test that search is case-insensitive."""
        results_lower = AIService.search_precedents("property")
        results_upper = AIService.search_precedents("PROPERTY")
        results_mixed = AIService.search_precedents("ProPerTy")
        
        assert len(results_lower) == len(results_upper) == len(results_mixed)
    
    def test_search_precedents_includes_relevance_score(self):
        """Test that results include relevance_score."""
        results = AIService.search_precedents("property")
        
        assert len(results) > 0
        for result in results:
            assert "relevance_score" in result
            assert result["relevance_score"] > 0
    
    def test_search_precedents_assault_keyword(self):
        """Test searching for assault-related precedents."""
        results = AIService.search_precedents("assault")
        
        assert len(results) > 0
        # Should find "Assault and Battery Case Law"
        assert any("assault" in r["title"].lower() for r in results)
    
    def test_search_precedents_contract_keyword(self):
        """Test searching for contract-related precedents."""
        results = AIService.search_precedents("contract")
        
        assert len(results) > 0
        # Should find "Contract Breach Remedies"
        assert any("contract" in r["title"].lower() for r in results)
    
    def test_search_precedents_emergency_keyword(self):
        """Test searching for emergency-related precedents."""
        results = AIService.search_precedents("emergency")
        
        assert len(results) > 0
        # Should find "Emergency Injunction Standards"
        assert any("emergency" in r["title"].lower() for r in results)


class TestAIServiceIntegration:
    """Test integration of AI services."""
    
    def test_triage_then_summarize(self, test_db: Session, citizen_user: User):
        """Test triaging a case then generating summary."""
        description = "I was urgently assaulted and need immediate help"
        case = CaseService.create_case(
            title="Urgent Assault Case",
            description=description,
            user_id=citizen_user.id,
            db=test_db
        )
        
        # Triage
        triaged_case = AIService.triage_case(case.id, description, test_db)
        assert triaged_case.priority == "HIGH"
        
        # Summarize
        summarized_case = AIService.generate_summary(case.id, description, test_db)
        assert "[AI Generated Summary]" in summarized_case.ai_summary
        
        # Verify both operations persisted
        final_case = test_db.query(Case).filter(Case.id == case.id).first()
        assert final_case.priority == "HIGH"
        assert "[AI Generated Summary]" in final_case.ai_summary
    
    def test_search_and_triage_workflow(self, test_db: Session, citizen_user: User):
        """Test searching precedents and triaging a related case."""
        # Search for assault precedents
        precedents = AIService.search_precedents("assault")
        assert len(precedents) > 0
        
        # Create and triage an assault case
        case = CaseService.create_case(
            title="Assault Case",
            description="I was assaulted by someone",
            user_id=citizen_user.id,
            db=test_db
        )
        
        triaged_case = AIService.triage_case(case.id, case.description, test_db)
        assert triaged_case.priority == "HIGH"
