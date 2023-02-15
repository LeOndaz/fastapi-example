from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Wiki
from schemas.wiki import WikiCreate, WikiResponse


def create_wiki(db: Session, data: WikiCreate):
    wiki = Wiki(**data.dict())
    db.add(wiki)
    db.commit()

    return WikiResponse(
        id=wiki.id,
        name=wiki.name,
    )


def get_wiki_by_id(db: Session, id: int):
    return db.get(Wiki, id)
