from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models import Document
from models.document import DocumentRevision
from schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentRevisionCreate,
    DocumentRevisionResponse,
)

from .wiki import get_wiki_by_id


def create_document(db: Session, data: DocumentCreate) -> Document:
    try:
        wiki = get_wiki_by_id(db, data.wiki_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="Wiki with id={} was not found".format(data.wiki_id)
        )

    content = data.content

    document = Document(
        title=data.title,
        wiki=wiki,
    )
    db.add(document)
    db.flush()

    default_revision = DocumentRevision(content=content, document_id=document.id)

    db.add(default_revision)
    db.commit()

    return document


def get_documents(db: Session, limit, offset) -> List[Document]:
    stmt = select(Document).limit(limit).offset(offset)
    return db.scalars(stmt).all()


def get_document_by_title(db: Session, title: str) -> Document:
    stmt = select(Document).where(Document.title.is_(title))
    return db.scalars(stmt).one()


def get_revision_by_title_and_timestamp(
    db: Session, title: str, timestamp: str
) -> DocumentRevision:
    timestamp_iso = datetime.fromisoformat(timestamp)

    stmt = (
        select(DocumentRevision)
        .join(Document)
        .filter(Document.title.is_(title))
        .filter(DocumentRevision.created_at == timestamp_iso)
    )

    return db.scalars(stmt).one()


def get_latest_revision(db: Session, document: Document) -> DocumentRevision:
    return document.revisions.order_by(DocumentRevision.created_at.desc()).first()


def create_revision(
    db: Session, title: str, data: DocumentRevisionCreate
) -> DocumentRevision:
    document = get_document_by_title(db, title)

    revision = DocumentRevision(
        document_id=document.id,
        content=data.content,
    )
    db.add(revision)
    db.commit()

    return revision
