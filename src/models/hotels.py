from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.models.base import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
