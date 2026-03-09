"""
Integration tests for case management API endpoints.

Tests cover:
- POST /api/cases: Create case (citizen only)
- GET /api/cases: List cases (role-based)
- GET /api/cases/{id}: Get case details (with authorization)
- PATCH /api/cases/{id}/status: Update status (judge only)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from services.auth import AuthService, UserCreate


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


class TestCreateCaseEndpoint:
    """Test POST /api/cases endpoint."""
    
    def test_citizen_can_create_case(self, client: TestClient, citizen_token: str):
        """Test that citizen can create a case."""
        response = client.post(
            "/api/cases",
            json={
                "title": "Property Dispute",
                "description": "Dispute over property ownership between neighbors"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Property Dispute"
        assert data["status"] == "FILED"
        assert "id" in data
    
    def test_judge_cannot_create_case(self, client: TestClient, judge_token: str):
        """Test that judge cannot create a case."""
        response = client.post(
            "/api/cases",
            json={
                "title": "Property Dispute",
                "description": "Dispute over property ownership"
            },
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 403
        assert "Only citizens" in response.json()["detail"]
    
    def test_create_case_without_auth_fails(self, client: TestClient):
        """Test that creating case without auth fails."""
        response = client.post(
            "/api/cases",
            json={
                "title": "Property Dispute",
                "description": "Dispute over property ownership"
            }
        )
        
        assert response.status_code == 401  # Missing credentials returns 401
    
    def test_create_case_with_empty_title_fails(self, client: TestClient, citizen_token: str):
        """Test that empty title fails."""
        response = client.post(
            "/api/cases",
            json={
                "title": "",
                "description": "Valid description"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 422
    
    def test_create_case_with_long_title_fails(self, client: TestClient, citizen_token: str):
        """Test that title longer than 200 chars fails."""
        response = client.post(
            "/api/cases",
            json={
                "title": "a" * 201,
                "description": "Valid description"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 422


class TestListCasesEndpoint:
    """Test GET /api/cases endpoint."""
    
    def test_citizen_sees_only_own_cases(self, client: TestClient, citizen_token: str):
        """Test that citizen sees only their own cases."""
        # Create a case
        client.post(
            "/api/cases",
            json={
                "title": "My Case",
                "description": "My case description"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        # List cases
        response = client.get(
            "/api/cases",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["cases"]) == 1
    
    def test_judge_sees_all_cases(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test that judge sees all cases."""
        # Create a case as citizen
        client.post(
            "/api/cases",
            json={
                "title": "Citizen's Case",
                "description": "Case filed by citizen"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        # List cases as judge
        response = client.get(
            "/api/cases",
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["cases"]) == 1
    
    def test_list_cases_pagination(self, client: TestClient, citizen_token: str):
        """Test pagination in case listing."""
        # Create 15 cases
        for i in range(15):
            client.post(
                "/api/cases",
                json={
                    "title": f"Case {i+1}",
                    "description": f"Case {i+1} description"
                },
                headers={"Authorization": f"Bearer {citizen_token}"}
            )
        
        # Get first page
        response1 = client.get(
            "/api/cases?page=1&limit=10",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        # Get second page
        response2 = client.get(
            "/api/cases?page=2&limit=10",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert len(data1["cases"]) == 10
        assert len(data2["cases"]) == 5
        assert data1["total"] == 15


class TestGetCaseEndpoint:
    """Test GET /api/cases/{id} endpoint."""
    
    def test_citizen_can_view_own_case(self, client: TestClient, citizen_token: str):
        """Test that citizen can view their own case."""
        # Create a case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "My Case",
                "description": "My case description"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Get case
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == case_id
        assert data["title"] == "My Case"
    
    def test_citizen_cannot_view_other_case(self, client: TestClient, citizen_token: str):
        """Test that citizen cannot view another citizen's case."""
        # Create a case as first citizen
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Other's Case",
                "description": "Another citizen's case"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Register another citizen
        other_response = client.post(
            "/api/auth/register",
            json={
                "email": "other@example.com",
                "password": "otherpass123",
                "role": "CITIZEN"
            }
        )
        other_token = other_response.json()["access_token"]
        
        # Try to get case as other citizen
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        
        assert response.status_code == 403
    
    def test_judge_can_view_any_case(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test that judge can view any case."""
        # Create a case as citizen
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Any Case",
                "description": "Case for judge to view"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Get case as judge
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == case_id
    
    def test_get_nonexistent_case_fails(self, client: TestClient, citizen_token: str):
        """Test that getting non-existent case fails."""
        response = client.get(
            "/api/cases/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 404


class TestUpdateCaseStatusEndpoint:
    """Test PATCH /api/cases/{id}/status endpoint."""
    
    def test_judge_can_update_case_status(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test that judge can update case status."""
        # Create a case as citizen
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Case to Update",
                "description": "Case for status update"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Update status as judge
        response = client.patch(
            f"/api/cases/{case_id}/status",
            json={"status": "IN_REVIEW"},
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "IN_REVIEW"
    
    def test_citizen_cannot_update_case_status(self, client: TestClient, citizen_token: str):
        """Test that citizen cannot update case status."""
        # Create a case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Case to Update",
                "description": "Case for status update"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Try to update status as citizen
        response = client.patch(
            f"/api/cases/{case_id}/status",
            json={"status": "IN_REVIEW"},
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert response.status_code == 403
    
    def test_update_with_invalid_status_fails(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test that invalid status fails."""
        # Create a case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Case to Update",
                "description": "Case for status update"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Try to update with invalid status
        response = client.patch(
            f"/api/cases/{case_id}/status",
            json={"status": "INVALID_STATUS"},
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert response.status_code == 400


class TestCaseFlow:
    """Test complete case management flows."""
    
    def test_citizen_files_case_judge_reviews(self, client: TestClient, citizen_token: str, judge_token: str):
        """Test complete flow: citizen files case, judge reviews and updates status."""
        # Citizen files case
        create_response = client.post(
            "/api/cases",
            json={
                "title": "Property Dispute",
                "description": "Dispute over property ownership"
            },
            headers={"Authorization": f"Bearer {citizen_token}"}
        )
        
        assert create_response.status_code == 201
        case_id = create_response.json()["id"]
        
        # Judge views case
        view_response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert view_response.status_code == 200
        assert view_response.json()["status"] == "FILED"
        
        # Judge updates status
        update_response = client.patch(
            f"/api/cases/{case_id}/status",
            json={"status": "IN_REVIEW"},
            headers={"Authorization": f"Bearer {judge_token}"}
        )
        
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "IN_REVIEW"
