from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Basic liveness check. Confirms the API process is up and responding.
    """
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Readiness check. Confirms the app can actually reach its dependencies —
    right now just the database. Deployment platforms (Railway, Render) can
    poll this to decide whether to route real traffic to this instance.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": f"unreachable: {str(e)}"}