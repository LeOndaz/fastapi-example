from pydantic import BaseModel


class WikiResponse(BaseModel):
    id: int
    name: str


class WikiCreate(BaseModel):
    name: str
