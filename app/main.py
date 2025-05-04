from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import router as router_ai_agent
from app.chroma_client.chroma_store import chroma_vectorstore
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await chroma_vectorstore.init()
    app.include_router(router_ai_agent)
    app.include_router(router_users)
    yield
    await chroma_vectorstore.close()


app = FastAPI(lifespan=lifespan)
