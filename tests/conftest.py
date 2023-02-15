import pytest

from db import engine, get_db
from models import Base, Document, DocumentRevision, Wiki


@pytest.fixture()
def engine_fixture():
    """
    Should use a better db ~_~
    """
    return engine


@pytest.fixture()
def db():
    db = next(get_db())
    return db


@pytest.fixture()
def clean_db(engine_fixture):
    Base.metadata.drop_all(bind=engine_fixture)
    Base.metadata.create_all(bind=engine_fixture)


@pytest.fixture()
def init_data(clean_db, db):
    wiki = Wiki(name="Big wiki")
    db.flush()

    for i in range(50):
        document = Document(title="Document {}".format(i + 1), wiki=wiki)

        for j in range(10):
            revision = DocumentRevision(content="Content {}".format(j + 1))
            document.revisions.add(revision)

        db.add(document)

    db.commit()
