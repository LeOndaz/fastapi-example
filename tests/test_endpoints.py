import pytest
from . import client


def test_root_works():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_wiki(clean_db, db):
    response = client.post("/wikis", json={"name": "Smol wiki"})

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["id"]
    assert response.json()["name"] == "Smol wiki"


def test_get_documents():
    response = client.get("/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_document():
    response = client.post(
        "/documents",
        json={"wiki": 1, "title": "Big document", "content": "Big Document Body"},
    )

    assert response.status_code == 200
    assert response.json()["wiki"] == 1
    assert response.json()["title"] == "Big document"
    assert response.json()["revisions"][0]["content"] == "Big Document Body"


def test_document_with_more_than_50_length_title():
    response = client.post(
        "/documents",
        json={
            "wiki": 1,
            "title": "".join([str(i) for i in range(100)]),
            "content": "Big Document Body",
        },
    )

    assert response.status_code == 422


def test_create_revision(init_data, clean_db, db):
    response = client.post("/documents/Document 1", json={"content": "Some revision"})

    assert response.status_code == 200
    assert response.json()["document"] == 1
    assert response.json()["content"] == "Some revision"
