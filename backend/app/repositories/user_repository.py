from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Encapsulates all database access for the User model.
    Used by the auth service (Phase 15) for signup/login flows.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, email: str, hashed_password: str) -> User:
        """Insert a new user. Password must already be hashed by the caller —
        this repository never handles raw passwords or hashing logic itself."""
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Used during login to look up a user by their email before verifying password."""
        return self.db.query(User).filter(User.email == email).first()