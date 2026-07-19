from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings

settings = get_settings()

# check_same_thread=False is SQLite-specific: SQLite normally restricts
# a connection to the thread that created it. FastAPI can serve requests
# on different threads, so we relax this — safe here since each request
# gets its own session (see get_db below), not a shared connection.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session per request.
    The `yield` pattern ensures the session is always closed after
    the request finishes, even if an error occurs mid-request.
    Usage in an endpoint: `db: Session = Depends(get_db)`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()