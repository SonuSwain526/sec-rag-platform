"""
User Database Model for sec-rag.

Defines the User model for local registration, identity verification, and permission checks.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class User(Base):
    """
    SQLAlchemy model representing application users.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # TODO: Add relationships to user-owned queries or bookmarks
    
    def __repr__(self) -> str:
        return f"<User email={self.email} is_active={self.is_active}>"
