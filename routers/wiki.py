from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

import controllers.wiki as wiki_controllers
from db import get_db
from schemas.wiki import WikiCreate

router = APIRouter()


@router.post("/wikis", tags=["wikis"])
def create_wiki(data: WikiCreate, db: Session = Depends(get_db)):
    return wiki_controllers.create_wiki(db, data)
