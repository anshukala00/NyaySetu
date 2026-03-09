"""
Password hashing and verification utilities using bcrypt.

This module provides secure password hashing with bcrypt (cost factor 12)
as per NFR2.1 security requirements.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
        
    Raises:
        ValueError: If password is empty or None
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(hashed)
        $2b$12$...
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt with cost factor 12 and hash the password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        # Convert both to bytes
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Verify password
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        # If any error occurs during verification, return False
        return False
