from typing import List

from pydantic import BaseModel, constr


class DocumentRevisionCreate(BaseModel):
    content: str


class DocumentRevisionResponse(BaseModel):
    id: int
    created_at: str
    document: int
    content: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    wiki: int
    revisions: List[DocumentRevisionResponse]


class DocumentCreate(BaseModel):
    wiki_id: int
    title: constr(max_length=50)
    content: str
