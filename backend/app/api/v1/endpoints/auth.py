"""
Authentication Endpoint Router for sec-rag.

Exposes auth endpoints for token generation, validation, and OAuth2 compatibility.
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.session import get_db

router = APIRouter()


@router.post("/login/access-token", response_model=dict)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, retrieve a JWT access token for future API requests.
    """
    # TODO: Load user from DB using user repository, verify password, return token
    # Mocking successful login for a user
    if form_data.username == "admin@secrag.com" and form_data.password == "adminpass":
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token("admin@secrag.com", expires_delta=access_token_expires),
            "token_type": "bearer",
        }
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect email or password"
    )


@router.post("/test-token", response_model=dict)
async def test_token() -> Any:
    """
    Test access token validation.
    """
    # TODO: Add Depends(get_current_user) check
    return {"message": "Token is valid"}
