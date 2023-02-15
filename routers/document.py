from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import controllers.document as document_controller
from db import get_db
from schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentRevisionCreate,
    DocumentRevisionResponse,
)
from shared.utils import document_to_pydantic, get_document_or_404, revision_to_pydantic

router = APIRouter()


@router.get("/documents", tags=["documents"])
async def get_documents(db: Session = Depends(get_db)) -> List[DocumentResponse]:
    """
    Retrieves the first 100 documents from the DB.
    """
    documents = document_controller.get_documents(db, 100, 0)
    return list(map(document_to_pydantic, documents))


@router.post("/documents", tags=["documents"])
async def create_document(
    data: DocumentCreate, db: Session = Depends(get_db)
) -> DocumentResponse:
    """
    Creates a document
    """
    document = document_controller.create_document(db, data)
    return document_to_pydantic(document)


@router.get("/documents/{title}", tags=["documents"])
async def get_revisions(
    title: str, db: Session = Depends(get_db)
) -> List[DocumentRevisionResponse]:
    """
    Returns a list of revisions of a specific document by it's id
    """
    document = get_document_or_404(db, title)
    return list(map(revision_to_pydantic, document.revisions))


@router.get("/documents/{title}/{timestamp}", tags=["documents"])
async def get_revision(
    title: str, timestamp: str, db: Session = Depends(get_db)
) -> DocumentRevisionResponse:
    """
    Returns a specific revision of a specific document by document id & revision timestamp
    """

    try:
        revision = document_controller.get_revision_by_title_and_timestamp(
            db, title, timestamp
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Revision for document={title} with timestamp={timestamp} was not found".format(
                title=title,
                timestamp=timestamp,
            ),
        )
    return revision_to_pydantic(revision)


@router.get("/document/{title}/latest", tags=["documents"])
async def get_latest(
    title: str, db: Session = Depends(get_db)
) -> DocumentRevisionResponse:
    """
    Returns the latest revision of a specific document by its id
    """
    document = get_document_or_404(db, title)
    revision = document_controller.get_latest_revision(db, document)
    return revision_to_pydantic(revision)


@router.post("/document/{title}", tags=["documents"])
async def create_revision(
    title: str, data: DocumentRevisionCreate, db: Session = Depends(get_db)
) -> DocumentRevisionResponse:
    """
    Creates a new revision for a document by its id
    """

    revision = document_controller.create_revision(db, title, data)
    return revision_to_pydantic(revision)
