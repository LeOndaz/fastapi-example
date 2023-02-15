import sqlite3

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models import Wiki
from schemas.wiki import WikiCreate, WikiResponse


def create_wiki(db: Session, data: WikiCreate):
    wiki = Wiki(**data.dict())
    db.add(wiki)
    db.commit()

    return wiki


def get_wiki_by_id(db: Session, id: int):
    wiki = db.get(Wiki, id)

    if wiki is None:
        raise NoResultFound

    return wiki
