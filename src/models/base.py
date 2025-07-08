from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False
    )
