from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class all ORM models inherit from.
    SQLAlchemy uses this to discover tables and generate the schema.
    Alembic also imports this to auto-detect model changes.
    """
    pass