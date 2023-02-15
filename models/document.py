from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class DocumentRevision(Base):
    __tablename__ = "document_revisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="revisions")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    wiki_id = Column(Integer, ForeignKey("wikis.id"), nullable=False)
    wiki = relationship("Wiki", back_populates="documents")

    revisions = relationship("DocumentRevision", lazy="dynamic")

    def __repr__(self):
        return self.title
