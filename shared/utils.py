from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import controllers.document as document_controller
from models import Document, DocumentRevision
from schemas.document import DocumentResponse, DocumentRevisionResponse


def revision_to_pydantic(revision: DocumentRevision):
    return DocumentRevisionResponse(
        id=revision.id,
        content=revision.content,
        document=revision.document.id,
        created_at=revision.created_at.isoformat(),
    )


def document_to_pydantic(document: Document):
    return DocumentResponse(
        id=document.id,
        title=document.title,
        wiki=document.wiki_id,
        revisions=list(map(revision_to_pydantic, document.revisions)),
    )


def get_document_or_404(db: Session, title: str):
    try:
        document = document_controller.get_document_by_title(db, title)
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="Document with title={} was not found".format(title)
        )

    return document
