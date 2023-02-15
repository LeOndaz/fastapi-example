from fastapi import FastAPI

from db import engine
from models.base import Base
from routers import document_router, wiki_router

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(document_router)
app.include_router(wiki_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
