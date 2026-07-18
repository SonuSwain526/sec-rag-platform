"""
Database Session Management Module for sec-rag.

This module initializes the SQLAlchemy 2.x database engine and session maker,
and defines dependencies for database session injection in FastAPI routes.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Create async engine for PostgreSQL connection
# TODO: Adjust connection pool parameters (pool_size, max_overflow) for production
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Async session factory
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.x Declarative Base for models.
    """
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding an active asynchronous database session.
    Automatically handles transaction close/rollback on completion.
    """
    async with async_session_maker() as session:
        try:
            yield session
            # TODO: Automatically commit changes if no exceptions were raised
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
