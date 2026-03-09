"""
Integration tests for AI API endpoints.

Tests cover:
- POST /api/triage/{case_id}: Triage endpoint
- POST /api/ai/summarize/{case_id}: Summarize endpoint
- GET /api/precedents/search: Search endpoint
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


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
    
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    yield db
    db.close()


@pytest.fixture
def client(test_db):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def citizen_token(client: TestClient):
    """Register and login a citizen user."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "citizen@example.com",
            "password": "citizenpass123",
            "role": "CITIZEN"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def judge_token(client: TestClient):
    """Register and login a judge user."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "judge@example.com",
            "password": "judgepass123",
            "role": "JUDGE"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def case_id(client: TestClient, citizen_token: str):
    """Create a test case and return its ID."""
    response = client.post(
        "/api/cases",
        json={
            "title": "Test Case",
            "description": "This is a test case for AI services"
        },
        headers={"Authorization": f"Bearer {citizen_token}"}
    )
    return response.json()["id"]


class TestTriageEndpoint:
    """Test POST /api/triage/{case_id} endpoint."""
    
    def test_triage_urgent_case(self, client: TestClient, citizen_token: str):
        """Test triaging an urgent case."""
        # Create urgent case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Assault Case",
                "description": "I was assaulted by my neighbor"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Triage case
        response = client.post(
            f"/api/triage/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "HIGH"
        assert data["case_id"] == case_id
    
    def test_triage_regular_case(self, client: TestClient, citizen_token: str):
        """Test triaging a regular case."""
        # Create regular case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Property Dispute",
                "description": "I have a dispute with my neighbor about property"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Triage case
        response = client.post(
            f"/api/triage/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "REGULAR"
    
    def test_triage_nonexistent_case(self, client: TestClient, citizen_token: str):
        """Test triaging non-existent case returns 404."""
        response = client.post(
            "/api/triage/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 404
    
    def test_triage_without_auth(self, client: TestClient, case_id: str):
        """Test triaging without authentication fails."""
        response = client.post(f"/api/triage/{case_id}")
        
        assert response.status_code == 401
    
    def test_triage_judge_can_triage_any_case(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test that judge can triage any case."""
        # Create case as citizen
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Urgent Case",
                "description": "This is urgent"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Triage as judge
        response = client.post(
            f"/api/triage/{case_id}",
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 200


class TestSummarizeEndpoint:
    """Test POST /api/ai/summarize/{case_id} endpoint."""
    
    def test_summarize_case(self, client: TestClient, citizen_token: str):
        """Test generating summary for a case."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Test Case",
                "description": "This is a test case description for summarization"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Summarize case
        response = client.post(
            f"/api/ai/summarize/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "[AI Generated Summary]" in data["ai_summary"]
        assert data["case_id"] == case_id
    
    def test_summarize_long_description(self, client: TestClient, citizen_token: str):
        """Test summarizing a case with long description."""
        long_description = "a" * 300
        
        # Create case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Long Case",
                "description": long_description
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Summarize case
        response = client.post(
            f"/api/ai/summarize/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        # Should be truncated to 200 chars + "..." + " [AI Generated Summary]"
        assert len(data["ai_summary"]) < len(long_description)
        assert "[AI Generated Summary]" in data["ai_summary"]
    
    def test_summarize_nonexistent_case(self, client: TestClient, citizen_token: str):
        """Test summarizing non-existent case returns 404."""
        response = client.post(
            "/api/ai/summarize/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 404
    
    def test_summarize_without_auth(self, client: TestClient, case_id: str):
        """Test summarizing without authentication fails."""
        response = client.post(f"/api/ai/summarize/{case_id}")
        
        assert response.status_code == 401


class TestSearchPrecedentsEndpoint:
    """Test GET /api/precedents/search endpoint."""
    
    def test_search_precedents_property(self, client: TestClient, citizen_token: str):
        """Test searching for property-related precedents."""
        response = client.get(
            "/api/precedents/search?q=property",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "property"
        assert len(data["results"]) > 0
        assert data["total"] > 0
    
    def test_search_precedents_assault(self, client: TestClient, citizen_token: str):
        """Test searching for assault-related precedents."""
        response = client.get(
            "/api/precedents/search?q=assault",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "assault"
        assert len(data["results"]) > 0
    
    def test_search_precedents_multiple_keywords(self, client: TestClient, citizen_token: str):
        """Test searching with multiple keywords."""
        response = client.get(
            "/api/precedents/search?q=property%20dispute",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) > 0
    
    def test_search_precedents_no_matches(self, client: TestClient, citizen_token: str):
        """Test searching with query that has no matches."""
        response = client.get(
            "/api/precedents/search?q=xyz123nonexistent",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 0
        assert data["total"] == 0
    
    def test_search_precedents_without_query(self, client: TestClient, citizen_token: str):
        """Test searching without query parameter fails."""
        response = client.get(
            "/api/precedents/search",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 422
    
    def test_search_precedents_without_auth(self, client: TestClient):
        """Test searching without authentication fails."""
        response = client.get("/api/precedents/search?q=property")
        
        assert response.status_code == 401
    
    def test_search_precedents_results_ranked(self, client: TestClient, citizen_token: str):
        """Test that search results are ranked by relevance."""
        response = client.get(
            "/api/precedents/search?q=property",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Results should be sorted by relevance_score (descending)
        for i in range(len(data["results"]) - 1):
            assert data["results"][i]["relevance_score"] >= data["results"][i + 1]["relevance_score"]
    
    def test_search_precedents_judge_can_search(self, client: TestClient, judge_token: str):
        """Test that judge can search precedents."""
        response = client.get(
            "/api/precedents/search?q=property",
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 200


class TestAIWorkflow:
    """Test complete AI workflows."""
    
    def test_triage_and_summarize_workflow(self, client: TestClient, citizen_token: str):
        """Test complete workflow: create case, triage, and summarize."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Urgent Case",
                "description": "I was urgently assaulted and need immediate help"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Triage
        triage_response = client.post(
            f"/api/triage/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        assert triage_response.status_code == 200
        assert triage_response.json()["priority"] == "HIGH"
        
        # Summarize
        summary_response = client.post(
            f"/api/ai/summarize/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        assert summary_response.status_code == 200
        assert "[AI Generated Summary]" in summary_response.json()["ai_summary"]
    
    def test_search_and_triage_workflow(self, client: TestClient, citizen_token: str):
        """Test workflow: search precedents, then triage related case."""
        # Search for assault precedents
        search_response = client.get(
            "/api/precedents/search?q=assault",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        assert search_response.status_code == 200
        assert len(search_response.json()["results"]) > 0
        
        # Create and triage assault case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Assault Case",
                "description": "I was assaulted"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        triage_response = client.post(
            f"/api/triage/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        assert triage_response.status_code == 200
        assert triage_response.json()["priority"] == "HIGH"
