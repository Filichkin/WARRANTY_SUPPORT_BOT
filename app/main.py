from redis import asyncio as aioredis

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.staticfiles import StaticFiles

from app.admin.models import Admin
from app.chroma_client.router import router as router_ai_agent
from app.chroma_client.chroma_store import chroma_vectorstore
from app.pages.router import router as router_pages
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await chroma_vectorstore.init()
    redis = aioredis.from_url(
        'redis://redis:6379',
        decode_responses=True,
        encoding='utf8',
    )
    await admin_app.configure(
        providers=[UsernamePasswordProvider(admin_model=Admin)],
        redis=redis,
    )
    app.include_router(router_ai_agent)
    app.include_router(router_users)
    app.include_router(router_pages)
    app.mount('/static', StaticFiles(directory='app/static'), name='static')
    app.mount('/admin', admin_app)
    yield
    await chroma_vectorstore.close()


app = FastAPI(lifespan=lifespan)
