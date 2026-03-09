"""
Unit tests for authentication service.

Tests cover:
- User registration with email validation and password hashing
- User login with credential verification
- Email uniqueness validation
- Password length validation
- JWT token generation
- Error handling (duplicate email, invalid credentials)
"""

import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from models.user import User
from models.case import Case
from app.database import Base
from services.auth import AuthService, UserCreate, UserLogin, TokenResponse
from services.password import verify_password
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
    yield db
    db.close()


class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_user_with_valid_data(self, test_db: Session):
        """Test successful user registration."""
        user_data = UserCreate(
            email="citizen@example.com",
            password="securepass123",
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.access_token is not None
        assert response.token_type == "bearer"
        assert response.role == "CITIZEN"
        assert response.user_id is not None
    
    def test_register_user_creates_database_record(self, test_db: Session):
        """Test that registration creates a user record in database."""
        user_data = UserCreate(
            email="judge@example.com",
            password="judgepass123",
            role="JUDGE"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        # Query database to verify user was created
        user = test_db.query(User).filter(User.email == "judge@example.com").first()
        
        assert user is not None
        assert user.email == "judge@example.com"
        assert user.role == "JUDGE"
        assert user.id == response.user_id
    
    def test_register_user_hashes_password(self, test_db: Session):
        """Test that password is hashed before storing."""
        user_data = UserCreate(
            email="user@example.com",
            password="plainpassword123",
            role="CITIZEN"
        )
        
        AuthService.register_user(user_data, test_db)
        
        # Query database and verify password is hashed
        user = test_db.query(User).filter(User.email == "user@example.com").first()
        
        assert user.password_hash != "plainpassword123"
        assert verify_password("plainpassword123", user.password_hash)
    
    def test_register_user_with_duplicate_email_raises_error(self, test_db: Session):
        """Test that registering with duplicate email raises 400 error."""
        user_data1 = UserCreate(
            email="duplicate@example.com",
            password="password123",
            role="CITIZEN"
        )
        user_data2 = UserCreate(
            email="duplicate@example.com",
            password="different123",
            role="JUDGE"
        )
        
        # Register first user
        AuthService.register_user(user_data1, test_db)
        
        # Try to register second user with same email
        with pytest.raises(Exception) as exc_info:
            AuthService.register_user(user_data2, test_db)
        
        assert "Email already registered" in str(exc_info.value)
    
    def test_register_user_returns_valid_token(self, test_db: Session):
        """Test that registration returns a valid JWT token."""
        user_data = UserCreate(
            email="tokentest@example.com",
            password="tokenpass123",
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        # Verify token is valid and contains correct claims
        payload = verify_token(response.access_token)
        
        assert payload["sub"] == str(response.user_id)
        assert payload["role"] == "CITIZEN"
    
    def test_register_citizen_user(self, test_db: Session):
        """Test registering a citizen user."""
        user_data = UserCreate(
            email="citizen@test.com",
            password="citizenpass123",
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.role == "CITIZEN"
    
    def test_register_judge_user(self, test_db: Session):
        """Test registering a judge user."""
        user_data = UserCreate(
            email="judge@test.com",
            password="judgepass123",
            role="JUDGE"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.role == "JUDGE"


class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_user_with_valid_credentials(self, test_db: Session):
        """Test successful login with valid credentials."""
        # Register user first
        user_data = UserCreate(
            email="login@example.com",
            password="loginpass123",
            role="CITIZEN"
        )
        AuthService.register_user(user_data, test_db)
        
        # Login with same credentials
        credentials = UserLogin(
            email="login@example.com",
            password="loginpass123"
        )
        response = AuthService.login_user(credentials, test_db)
        
        assert response.access_token is not None
        assert response.token_type == "bearer"
        assert response.role == "CITIZEN"
    
    def test_login_user_with_invalid_email_raises_error(self, test_db: Session):
        """Test that login with non-existent email raises 401 error."""
        credentials = UserLogin(
            email="nonexistent@example.com",
            password="anypassword123"
        )
        
        with pytest.raises(Exception) as exc_info:
            AuthService.login_user(credentials, test_db)
        
        assert "Invalid credentials" in str(exc_info.value)
    
    def test_login_user_with_wrong_password_raises_error(self, test_db: Session):
        """Test that login with wrong password raises 401 error."""
        # Register user
        user_data = UserCreate(
            email="wrongpass@example.com",
            password="correctpass123",
            role="CITIZEN"
        )
        AuthService.register_user(user_data, test_db)
        
        # Try to login with wrong password
        credentials = UserLogin(
            email="wrongpass@example.com",
            password="wrongpass123"
        )
        
        with pytest.raises(Exception) as exc_info:
            AuthService.login_user(credentials, test_db)
        
        assert "Invalid credentials" in str(exc_info.value)
    
    def test_login_returns_valid_token(self, test_db: Session):
        """Test that login returns a valid JWT token."""
        # Register user
        user_data = UserCreate(
            email="tokenlogin@example.com",
            password="tokenpass123",
            role="JUDGE"
        )
        register_response = AuthService.register_user(user_data, test_db)
        
        # Login
        credentials = UserLogin(
            email="tokenlogin@example.com",
            password="tokenpass123"
        )
        login_response = AuthService.login_user(credentials, test_db)
        
        # Verify token is valid
        payload = verify_token(login_response.access_token)
        
        assert payload["sub"] == str(register_response.user_id)
        assert payload["role"] == "JUDGE"
    
    def test_login_returns_correct_user_id(self, test_db: Session):
        """Test that login returns the correct user_id."""
        # Register user
        user_data = UserCreate(
            email="userid@example.com",
            password="userpass123",
            role="CITIZEN"
        )
        register_response = AuthService.register_user(user_data, test_db)
        
        # Login
        credentials = UserLogin(
            email="userid@example.com",
            password="userpass123"
        )
        login_response = AuthService.login_user(credentials, test_db)
        
        assert login_response.user_id == register_response.user_id
    
    def test_login_case_sensitive_email(self, test_db: Session):
        """Test that email login is case-sensitive."""
        # Register user with lowercase email
        user_data = UserCreate(
            email="casesensitive@example.com",
            password="casepass123",
            role="CITIZEN"
        )
        AuthService.register_user(user_data, test_db)
        
        # Try to login with uppercase email
        credentials = UserLogin(
            email="CASESENSITIVE@EXAMPLE.COM",
            password="casepass123"
        )
        
        # This should fail because email is case-sensitive in database
        with pytest.raises(Exception) as exc_info:
            AuthService.login_user(credentials, test_db)
        
        assert "Invalid credentials" in str(exc_info.value)


class TestPasswordValidation:
    """Test password validation in registration."""
    
    def test_register_with_password_too_short_raises_error(self):
        """Test that password shorter than 8 characters raises validation error."""
        user_data_dict = {
            "email": "short@example.com",
            "password": "short",
            "role": "CITIZEN"
        }
        
        with pytest.raises(Exception) as exc_info:
            UserCreate(**user_data_dict)
        
        assert "at least 8 characters" in str(exc_info.value)
    
    def test_register_with_password_exactly_8_chars(self, test_db: Session):
        """Test that password with exactly 8 characters is accepted."""
        user_data = UserCreate(
            email="eightchar@example.com",
            password="12345678",
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.access_token is not None
    
    def test_register_with_long_password(self, test_db: Session):
        """Test that long passwords (within bcrypt's 72-byte limit) are accepted."""
        # Bcrypt has a 72-byte limit, so use a password within that limit
        long_password = "a" * 70
        user_data = UserCreate(
            email="longpass@example.com",
            password=long_password,
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.access_token is not None


class TestEmailValidation:
    """Test email validation in registration."""
    
    def test_register_with_invalid_email_format_raises_error(self):
        """Test that invalid email format raises validation error."""
        user_data_dict = {
            "email": "notanemail",
            "password": "validpass123",
            "role": "CITIZEN"
        }
        
        with pytest.raises(Exception):
            UserCreate(**user_data_dict)
    
    def test_register_with_valid_email_formats(self, test_db: Session):
        """Test that various valid email formats are accepted."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@test-domain.org"
        ]
        
        for email in valid_emails:
            user_data = UserCreate(
                email=email,
                password="validpass123",
                role="CITIZEN"
            )
            
            response = AuthService.register_user(user_data, test_db)
            assert response.access_token is not None


class TestRoleValidation:
    """Test role validation in registration."""
    
    def test_register_with_invalid_role_raises_error(self):
        """Test that invalid role raises validation error."""
        user_data_dict = {
            "email": "invalid@example.com",
            "password": "validpass123",
            "role": "INVALID_ROLE"
        }
        
        with pytest.raises(Exception) as exc_info:
            UserCreate(**user_data_dict)
        
        assert "CITIZEN or JUDGE" in str(exc_info.value)
    
    def test_register_with_citizen_role(self, test_db: Session):
        """Test registration with CITIZEN role."""
        user_data = UserCreate(
            email="citizen@example.com",
            password="citizenpass123",
            role="CITIZEN"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.role == "CITIZEN"
    
    def test_register_with_judge_role(self, test_db: Session):
        """Test registration with JUDGE role."""
        user_data = UserCreate(
            email="judge@example.com",
            password="judgepass123",
            role="JUDGE"
        )
        
        response = AuthService.register_user(user_data, test_db)
        
        assert response.role == "JUDGE"


class TestAuthenticationFlow:
    """Test complete authentication flows."""
    
    def test_register_and_login_flow(self, test_db: Session):
        """Test complete flow: register user, then login."""
        # Register
        user_data = UserCreate(
            email="flow@example.com",
            password="flowpass123",
            role="CITIZEN"
        )
        register_response = AuthService.register_user(user_data, test_db)
        
        # Login
        credentials = UserLogin(
            email="flow@example.com",
            password="flowpass123"
        )
        login_response = AuthService.login_user(credentials, test_db)
        
        # Verify both responses have same user_id
        assert register_response.user_id == login_response.user_id
        assert register_response.role == login_response.role
    
    def test_multiple_users_registration(self, test_db: Session):
        """Test registering multiple users."""
        users = [
            UserCreate(email="user1@example.com", password="pass1234", role="CITIZEN"),
            UserCreate(email="user2@example.com", password="pass1234", role="JUDGE"),
            UserCreate(email="user3@example.com", password="pass1234", role="CITIZEN"),
        ]
        
        responses = []
        for user_data in users:
            response = AuthService.register_user(user_data, test_db)
            responses.append(response)
        
        # Verify all users have different IDs
        user_ids = [r.user_id for r in responses]
        assert len(user_ids) == len(set(user_ids))
    
    def test_each_user_can_login_independently(self, test_db: Session):
        """Test that each registered user can login independently."""
        # Register two users
        user1_data = UserCreate(
            email="user1@example.com",
            password="user1pass123",
            role="CITIZEN"
        )
        user2_data = UserCreate(
            email="user2@example.com",
            password="user2pass123",
            role="JUDGE"
        )
        
        AuthService.register_user(user1_data, test_db)
        AuthService.register_user(user2_data, test_db)
        
        # Login as user1
        creds1 = UserLogin(email="user1@example.com", password="user1pass123")
        response1 = AuthService.login_user(creds1, test_db)
        
        # Login as user2
        creds2 = UserLogin(email="user2@example.com", password="user2pass123")
        response2 = AuthService.login_user(creds2, test_db)
        
        # Verify different tokens and user IDs
        assert response1.access_token != response2.access_token
        assert response1.user_id != response2.user_id
        assert response1.role == "CITIZEN"
        assert response2.role == "JUDGE"
