from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.models.base import Base, TimestampMixin


class UsersOrm(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
