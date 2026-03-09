"""
Integration tests for authentication API endpoints.

Tests cover:
- POST /api/auth/register endpoint
- POST /api/auth/login endpoint
- Error handling (400, 401, 422)
- Request/response validation
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from services.jwt import verify_token


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


class TestRegisterEndpoint:
    """Test POST /api/auth/register endpoint."""
    
    def test_register_with_valid_data(self, client: TestClient):
        """Test successful registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "citizen@example.com",
                "password": "securepass123",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "CITIZEN"
        assert "user_id" in data
    
    def test_register_returns_valid_token(self, client: TestClient):
        """Test that registration returns a valid JWT token."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "tokentest@example.com",
                "password": "tokenpass123",
                "role": "JUDGE"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify token is valid
        payload = verify_token(data["access_token"])
        assert payload["role"] == "JUDGE"
    
    def test_register_with_duplicate_email(self, client: TestClient):
        """Test that duplicate email returns 400 error."""
        # Register first user
        client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "role": "CITIZEN"
            }
        )
        
        # Try to register second user with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "different123",
                "role": "JUDGE"
            }
        )
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_with_invalid_email(self, client: TestClient):
        """Test that invalid email format returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "notanemail",
                "password": "password123",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_with_short_password(self, client: TestClient):
        """Test that password shorter than 8 characters returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "short",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_with_invalid_role(self, client: TestClient):
        """Test that invalid role returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "password123",
                "role": "INVALID"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_missing_email(self, client: TestClient):
        """Test that missing email returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "password": "password123",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_missing_password(self, client: TestClient):
        """Test that missing password returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_missing_role(self, client: TestClient):
        """Test that missing role returns 422 error."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_citizen_role(self, client: TestClient):
        """Test registration with CITIZEN role."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "citizen@example.com",
                "password": "citizenpass123",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 201
        assert response.json()["role"] == "CITIZEN"
    
    def test_register_judge_role(self, client: TestClient):
        """Test registration with JUDGE role."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "judge@example.com",
                "password": "judgepass123",
                "role": "JUDGE"
            }
        )
        
        assert response.status_code == 201
        assert response.json()["role"] == "JUDGE"


class TestLoginEndpoint:
    """Test POST /api/auth/login endpoint."""
    
    def test_login_with_valid_credentials(self, client: TestClient):
        """Test successful login."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "loginpass123",
                "role": "CITIZEN"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "loginpass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "CITIZEN"
        assert "user_id" in data
    
    def test_login_returns_valid_token(self, client: TestClient):
        """Test that login returns a valid JWT token."""
        # Register user
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "tokenlogin@example.com",
                "password": "tokenpass123",
                "role": "JUDGE"
            }
        )
        register_user_id = register_response.json()["user_id"]
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "tokenlogin@example.com",
                "password": "tokenpass123"
            }
        )
        
        assert login_response.status_code == 200
        data = login_response.json()
        
        # Verify token is valid and contains correct claims
        payload = verify_token(data["access_token"])
        assert payload["role"] == "JUDGE"
        assert payload["sub"] == register_user_id
    
    def test_login_with_invalid_email(self, client: TestClient):
        """Test that login with non-existent email returns 401 error."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "anypassword123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_with_wrong_password(self, client: TestClient):
        """Test that login with wrong password returns 401 error."""
        # Register user
        client.post(
            "/api/auth/register",
            json={
                "email": "wrongpass@example.com",
                "password": "correctpass123",
                "role": "CITIZEN"
            }
        )
        
        # Try to login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": "wrongpass@example.com",
                "password": "wrongpass123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_missing_email(self, client: TestClient):
        """Test that missing email returns 422 error."""
        response = client.post(
            "/api/auth/login",
            json={
                "password": "password123"
            }
        )
        
        assert response.status_code == 422
    
    def test_login_missing_password(self, client: TestClient):
        """Test that missing password returns 422 error."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com"
            }
        )
        
        assert response.status_code == 422
    
    def test_login_with_invalid_email_format(self, client: TestClient):
        """Test that invalid email format returns 422 error."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "notanemail",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422


class TestAuthenticationFlow:
    """Test complete authentication flows."""
    
    def test_register_and_login_flow(self, client: TestClient):
        """Test complete flow: register user, then login."""
        # Register
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "flow@example.com",
                "password": "flowpass123",
                "role": "CITIZEN"
            }
        )
        register_data = register_response.json()
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "flow@example.com",
                "password": "flowpass123"
            }
        )
        login_data = login_response.json()
        
        # Verify both responses have same user_id and role
        assert register_data["user_id"] == login_data["user_id"]
        assert register_data["role"] == login_data["role"]
    
    def test_multiple_users_can_register_and_login(self, client: TestClient):
        """Test that multiple users can register and login independently."""
        users = [
            {"email": "user1@example.com", "password": "pass1234", "role": "CITIZEN"},
            {"email": "user2@example.com", "password": "pass1234", "role": "JUDGE"},
            {"email": "user3@example.com", "password": "pass1234", "role": "CITIZEN"},
        ]
        
        user_ids = []
        
        # Register all users
        for user in users:
            response = client.post("/api/auth/register", json=user)
            assert response.status_code == 201
            user_ids.append(response.json()["user_id"])
        
        # Verify all user IDs are different
        assert len(user_ids) == len(set(user_ids))
        
        # Login as each user
        for user in users:
            response = client.post(
                "/api/auth/login",
                json={"email": user["email"], "password": user["password"]}
            )
            assert response.status_code == 200
            assert response.json()["role"] == user["role"]
    
    def test_token_from_register_can_be_used(self, client: TestClient):
        """Test that token from registration can be used for authenticated requests."""
        # Register user
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "tokenuse@example.com",
                "password": "tokenpass123",
                "role": "CITIZEN"
            }
        )
        
        assert register_response.status_code == 201
        token = register_response.json()["access_token"]
        
        # Verify token is valid by decoding it
        payload = verify_token(token)
        assert "sub" in payload
        assert "role" in payload
        assert payload["role"] == "CITIZEN"


class TestErrorHandling:
    """Test error handling in auth endpoints."""
    
    def test_register_with_empty_body(self, client: TestClient):
        """Test that empty request body returns 422 error."""
        response = client.post("/api/auth/register", json={})
        assert response.status_code == 422
    
    def test_login_with_empty_body(self, client: TestClient):
        """Test that empty request body returns 422 error."""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422
    
    def test_register_response_structure(self, client: TestClient):
        """Test that register response has correct structure."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "structure@example.com",
                "password": "structpass123",
                "role": "CITIZEN"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response has all required fields
        assert "access_token" in data
        assert "token_type" in data
        assert "user_id" in data
        assert "role" in data
        
        # Verify field types
        assert isinstance(data["access_token"], str)
        assert isinstance(data["token_type"], str)
        assert isinstance(data["user_id"], str)
        assert isinstance(data["role"], str)
    
    def test_login_response_structure(self, client: TestClient):
        """Test that login response has correct structure."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "email": "loginstructure@example.com",
                "password": "structpass123",
                "role": "JUDGE"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "loginstructure@example.com",
                "password": "structpass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response has all required fields
        assert "access_token" in data
        assert "token_type" in data
        assert "user_id" in data
        assert "role" in data
