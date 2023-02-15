from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Wiki(Base):
    __tablename__ = "wikis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    documents = relationship("Document")

    def __repr__(self):
        return self.name
