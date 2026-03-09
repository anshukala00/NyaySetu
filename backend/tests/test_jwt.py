"""
Unit tests for JWT token generation and verification service.

Tests cover:
- JWT token generation with user_id and role claims
- Token expiration set to 24 hours
- Token verification and decoding
- get_current_user FastAPI dependency
- Edge cases and error handling
"""

import os
import pytest
from datetime import datetime, timedelta
from uuid import uuid4, UUID
from unittest.mock import Mock
from jose import jwt, JWTError
from fastapi import HTTPException

from services.jwt import (
    create_access_token,
    verify_token,
    get_current_user,
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRATION_HOURS
)


class TestCreateAccessToken:
    """Test JWT token generation functionality."""
    
    def test_create_access_token_with_valid_inputs(self):
        """Test that create_access_token generates a valid JWT token."""
        user_id = uuid4()
        role = "CITIZEN"
        
        token = create_access_token(user_id, role)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_contains_correct_claims(self):
        """Test that generated token contains user_id and role claims."""
        user_id = uuid4()
        role = "JUDGE"
        
        token = create_access_token(user_id, role)
        
        # Decode token without verification to check claims
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        assert payload["sub"] == str(user_id)
        assert payload["role"] == role
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_access_token_expiration_is_24_hours(self):
        """Test that token expiration is set to 24 hours from creation."""
        user_id = uuid4()
        role = "CITIZEN"
        
        before_creation = datetime.utcnow()
        token = create_access_token(user_id, role)
        after_creation = datetime.utcnow()
        
        # Decode token to check expiration
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        exp_timestamp = payload["exp"]
        iat_timestamp = payload["iat"]
        
        # Calculate the difference between exp and iat
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
        iat_datetime = datetime.utcfromtimestamp(iat_timestamp)
        time_diff = exp_datetime - iat_datetime
        
        # Should be exactly 24 hours (with small tolerance for processing time)
        expected_seconds = 24 * 60 * 60
        assert abs(time_diff.total_seconds() - expected_seconds) < 2  # 2 second tolerance
    
    def test_create_access_token_with_citizen_role(self):
        """Test token generation with CITIZEN role."""
        user_id = uuid4()
        role = "CITIZEN"
        
        token = create_access_token(user_id, role)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        assert payload["role"] == "CITIZEN"
    
    def test_create_access_token_with_judge_role(self):
        """Test token generation with JUDGE role."""
        user_id = uuid4()
        role = "JUDGE"
        
        token = create_access_token(user_id, role)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        assert payload["role"] == "JUDGE"
    
    def test_create_access_token_with_invalid_role_raises_error(self):
        """Test that invalid role raises ValueError."""
        user_id = uuid4()
        
        with pytest.raises(ValueError, match="role must be either 'CITIZEN' or 'JUDGE'"):
            create_access_token(user_id, "INVALID_ROLE")
    
    def test_create_access_token_with_none_user_id_raises_error(self):
        """Test that None user_id raises ValueError."""
        with pytest.raises(ValueError, match="user_id cannot be None"):
            create_access_token(None, "CITIZEN")
    
    def test_create_access_token_different_tokens_for_same_user(self):
        """Test that creating multiple tokens for same user produces different tokens."""
        import time
        user_id = uuid4()
        role = "CITIZEN"
        
        token1 = create_access_token(user_id, role)
        time.sleep(1)  # Wait 1 second to ensure different iat timestamp
        token2 = create_access_token(user_id, role)
        
        # Tokens should be different due to different iat (issued at) times
        assert token1 != token2


class TestVerifyToken:
    """Test JWT token verification functionality."""
    
    def test_verify_token_with_valid_token(self):
        """Test that verify_token successfully decodes a valid token."""
        user_id = uuid4()
        role = "CITIZEN"
        
        token = create_access_token(user_id, role)
        payload = verify_token(token)
        
        assert payload["sub"] == str(user_id)
        assert payload["role"] == role
    
    def test_verify_token_with_expired_token_raises_exception(self):
        """Test that verify_token raises HTTPException for expired token."""
        user_id = uuid4()
        role = "CITIZEN"
        
        # Create token with past expiration
        past_time = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": past_time,
            "iat": datetime.utcnow() - timedelta(hours=25)
        }
        expired_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(expired_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in exc_info.value.detail
    
    def test_verify_token_with_invalid_signature_raises_exception(self):
        """Test that verify_token raises HTTPException for token with invalid signature."""
        user_id = uuid4()
        role = "CITIZEN"
        
        # Create token with wrong secret
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        invalid_token = jwt.encode(payload, "wrong_secret", algorithm=JWT_ALGORITHM)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in exc_info.value.detail
    
    def test_verify_token_with_malformed_token_raises_exception(self):
        """Test that verify_token raises HTTPException for malformed token."""
        malformed_token = "not.a.valid.jwt.token"
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(malformed_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in exc_info.value.detail
    
    def test_verify_token_with_empty_token_raises_exception(self):
        """Test that verify_token raises HTTPException for empty token."""
        with pytest.raises(HTTPException) as exc_info:
            verify_token("")
        
        assert exc_info.value.status_code == 401
    
    def test_verify_token_preserves_all_claims(self):
        """Test that verify_token returns all token claims."""
        user_id = uuid4()
        role = "JUDGE"
        
        token = create_access_token(user_id, role)
        payload = verify_token(token)
        
        assert "sub" in payload
        assert "role" in payload
        assert "exp" in payload
        assert "iat" in payload


class TestGetCurrentUser:
    """Test get_current_user FastAPI dependency functionality."""
    
    def test_get_current_user_with_valid_token(self):
        """Test that get_current_user extracts user info from valid token."""
        user_id = uuid4()
        role = "CITIZEN"
        
        token = create_access_token(user_id, role)
        
        # Mock HTTPAuthRequest credentials
        mock_credentials = Mock()
        mock_credentials.credentials = token
        
        current_user = get_current_user(mock_credentials)
        
        assert current_user["user_id"] == user_id
        assert current_user["role"] == role
    
    def test_get_current_user_returns_uuid_type(self):
        """Test that get_current_user returns user_id as UUID type."""
        user_id = uuid4()
        role = "JUDGE"
        
        token = create_access_token(user_id, role)
        
        mock_credentials = Mock()
        mock_credentials.credentials = token
        
        current_user = get_current_user(mock_credentials)
        
        assert isinstance(current_user["user_id"], UUID)
    
    def test_get_current_user_with_expired_token_raises_exception(self):
        """Test that get_current_user raises HTTPException for expired token."""
        user_id = uuid4()
        role = "CITIZEN"
        
        # Create expired token
        past_time = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": past_time,
            "iat": datetime.utcnow() - timedelta(hours=25)
        }
        expired_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        mock_credentials = Mock()
        mock_credentials.credentials = expired_token
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == 401
    
    def test_get_current_user_with_invalid_token_raises_exception(self):
        """Test that get_current_user raises HTTPException for invalid token."""
        mock_credentials = Mock()
        mock_credentials.credentials = "invalid.token.here"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == 401
    
    def test_get_current_user_with_missing_sub_claim_raises_exception(self):
        """Test that get_current_user raises HTTPException when sub claim is missing."""
        # Create token without sub claim
        payload = {
            "role": "CITIZEN",
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        mock_credentials = Mock()
        mock_credentials.credentials = token
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token payload" in exc_info.value.detail
    
    def test_get_current_user_with_missing_role_claim_raises_exception(self):
        """Test that get_current_user raises HTTPException when role claim is missing."""
        user_id = uuid4()
        
        # Create token without role claim
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        mock_credentials = Mock()
        mock_credentials.credentials = token
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token payload" in exc_info.value.detail
    
    def test_get_current_user_with_invalid_uuid_raises_exception(self):
        """Test that get_current_user raises HTTPException for invalid UUID in token."""
        # Create token with invalid UUID string
        payload = {
            "sub": "not-a-valid-uuid",
            "role": "CITIZEN",
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        mock_credentials = Mock()
        mock_credentials.credentials = token
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == 401
        assert "Invalid user_id in token" in exc_info.value.detail


class TestJWTConfiguration:
    """Test JWT configuration and environment variables."""
    
    def test_jwt_secret_is_loaded(self):
        """Test that JWT_SECRET is loaded from environment."""
        assert JWT_SECRET is not None
        assert len(JWT_SECRET) > 0
    
    def test_jwt_algorithm_is_hs256(self):
        """Test that JWT_ALGORITHM is set to HS256."""
        assert JWT_ALGORITHM == "HS256"
    
    def test_jwt_expiration_hours_is_24(self):
        """Test that JWT_EXPIRATION_HOURS is set to 24."""
        assert JWT_EXPIRATION_HOURS == 24


class TestJWTTokenProperties:
    """Property-based tests for JWT token service."""
    
    def test_token_roundtrip_preserves_data(self):
        """Test that creating and verifying token preserves user data."""
        test_cases = [
            (uuid4(), "CITIZEN"),
            (uuid4(), "JUDGE"),
            (uuid4(), "CITIZEN"),
            (uuid4(), "JUDGE"),
        ]
        
        for user_id, role in test_cases:
            token = create_access_token(user_id, role)
            payload = verify_token(token)
            
            assert payload["sub"] == str(user_id)
            assert payload["role"] == role
    
    def test_different_users_produce_different_tokens(self):
        """Test that different users produce different tokens."""
        user_id1 = uuid4()
        user_id2 = uuid4()
        role = "CITIZEN"
        
        token1 = create_access_token(user_id1, role)
        token2 = create_access_token(user_id2, role)
        
        assert token1 != token2
        
        payload1 = verify_token(token1)
        payload2 = verify_token(token2)
        
        assert payload1["sub"] != payload2["sub"]
    
    def test_different_roles_produce_different_tokens(self):
        """Test that different roles produce different tokens."""
        user_id = uuid4()
        
        token_citizen = create_access_token(user_id, "CITIZEN")
        token_judge = create_access_token(user_id, "JUDGE")
        
        assert token_citizen != token_judge
        
        payload_citizen = verify_token(token_citizen)
        payload_judge = verify_token(token_judge)
        
        assert payload_citizen["role"] == "CITIZEN"
        assert payload_judge["role"] == "JUDGE"
