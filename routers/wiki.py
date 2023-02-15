import sqlite3

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

import controllers.wiki as wiki_controllers
from db import get_db
from schemas.wiki import WikiCreate, WikiResponse
from fastapi import Depends, HTTPException

router = APIRouter()


@router.post("/wikis", tags=["wikis"])
def create_wiki(data: WikiCreate, db: Session = Depends(get_db)) -> WikiResponse:
    try:
        wiki = wiki_controllers.create_wiki(db, data)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=401, detail="Wiki with name={} already exists".format(data.name)
        )

    return WikiResponse(id=wiki.id, name=wiki.name)
