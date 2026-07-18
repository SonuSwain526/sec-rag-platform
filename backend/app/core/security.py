"""
Security Utilities for sec-rag.

This module provides helpers for hashing passwords, generating JWT tokens,
and verifying security credentials.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context configuration
# TODO: Move to bcrypt or argon2 backend with custom tuning params if needed
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain text password matches a stored hashed password.
    """
    # TODO: Add rate limiting or telemetry notifications for failed checks
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generates a secure cryptographic hash for a plain text password.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a JWT access token for the authenticated user/service.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # TODO: Wrap key loading from config in an exception block for safety
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Decodes and verifies a JWT token. Returns the subject if valid, else None.
    """
    try:
        # TODO: Handle TokenExpired and InvalidToken specifically with custom exceptions
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
