"""
Unit tests for password hashing and verification utilities.

Tests cover:
- Password hashing with bcrypt cost factor 12
- Password verification
- Edge cases and error handling
"""

import pytest
from services.password import hash_password, verify_password


class TestPasswordHashing:
    """Test password hashing functionality."""
    
    def test_hash_password_returns_different_hash_each_time(self):
        """Test that hashing the same password twice produces different hashes (salt)."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
        assert hash1 != password
        assert hash2 != password
    
    def test_hash_password_produces_bcrypt_hash(self):
        """Test that hash_password produces a valid bcrypt hash format."""
        password = "mypassword"
        hashed = hash_password(password)
        
        # Bcrypt hashes start with $2b$ (or $2a$, $2y$)
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$") or hashed.startswith("$2y$")
        # Bcrypt hashes with cost factor 12 should have $12$ after the algorithm identifier
        assert "$12$" in hashed
    
    def test_hash_password_with_empty_string_raises_error(self):
        """Test that hashing an empty password raises ValueError."""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            hash_password("")
    
    def test_hash_password_with_none_raises_error(self):
        """Test that hashing None raises ValueError."""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            hash_password(None)
    
    def test_hash_password_with_long_password(self):
        """Test that hashing a long password works correctly.
        
        Note: Bcrypt has a 72-byte limit, so passwords longer than this
        will be truncated. This is a known bcrypt limitation.
        """
        long_password = "a" * 70  # Within bcrypt's 72-byte limit
        hashed = hash_password(long_password)
        
        assert hashed is not None
        assert len(hashed) > 0
        assert hashed != long_password
    
    def test_hash_password_with_special_characters(self):
        """Test that hashing passwords with special characters works."""
        password = "p@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password


class TestPasswordVerification:
    """Test password verification functionality."""
    
    def test_verify_password_with_correct_password(self):
        """Test that verify_password returns True for correct password."""
        password = "correctpassword"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_with_incorrect_password(self):
        """Test that verify_password returns False for incorrect password."""
        password = "correctpassword"
        hashed = hash_password(password)
        
        assert verify_password("wrongpassword", hashed) is False
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "MyPassword"
        hashed = hash_password(password)
        
        assert verify_password("mypassword", hashed) is False
        assert verify_password("MYPASSWORD", hashed) is False
        assert verify_password("MyPassword", hashed) is True
    
    def test_verify_password_with_empty_plain_password(self):
        """Test that verify_password returns False for empty plain password."""
        hashed = hash_password("somepassword")
        
        assert verify_password("", hashed) is False
    
    def test_verify_password_with_empty_hashed_password(self):
        """Test that verify_password returns False for empty hashed password."""
        assert verify_password("somepassword", "") is False
    
    def test_verify_password_with_none_values(self):
        """Test that verify_password returns False for None values."""
        hashed = hash_password("somepassword")
        
        assert verify_password(None, hashed) is False
        assert verify_password("somepassword", None) is False
        assert verify_password(None, None) is False
    
    def test_verify_password_with_special_characters(self):
        """Test that verification works with special characters."""
        password = "p@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("p@ssw0rd!#$%^&*()x", hashed) is False


class TestPasswordHashingProperties:
    """Property-based tests for password hashing."""
    
    def test_hash_never_equals_plaintext(self):
        """Test that hashed password never equals the plaintext password."""
        test_passwords = [
            "short",
            "mediumlength123",
            "verylongpasswordwithlotsofcharacters",  # Reasonable length
            "p@ssw0rd!",
            "12345678",
            "aBcDeFgH",
        ]
        
        for password in test_passwords:
            hashed = hash_password(password)
            assert hashed != password
    
    def test_verify_is_inverse_of_hash(self):
        """Test that verify_password is the inverse operation of hash_password."""
        test_passwords = [
            "password1",
            "password2",
            "p@ssw0rd!",
            "12345678",
            "aBcDeFgH123",
        ]
        
        for password in test_passwords:
            hashed = hash_password(password)
            assert verify_password(password, hashed) is True
    
    def test_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = hash_password(password1)
        hash2 = hash_password(password2)
        
        assert hash1 != hash2
