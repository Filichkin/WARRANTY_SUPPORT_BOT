from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastadmin import fastapi_app as admin_app
from fastadmin import register
from fastadmin import SqlAlchemyModelAdmin
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.chroma_client.router import router as router_ai_agent
from app.chroma_client.chroma_store import chroma_vectorstore
from app.pages.router import router as router_pages
from app.users.models import User
from app.users.router import router as router_users
from database import async_session_maker


@register(User, sqlalchemy_sessionmaker=async_session_maker)
class UserAdmin(SqlAlchemyModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_super_admin')
    list_display_links = ('id', 'email')

    async def authenticate(self, email, password):
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            query = select(self.model_cls).filter_by(
                email=email,
                password=password,
                is_super_admin=True
                )
            result = await session.scalars(query)
            obj = result.first()
            if not obj:
                return None
            return obj.id


@asynccontextmanager
async def lifespan(app: FastAPI):
    await chroma_vectorstore.init()
    app.include_router(router_ai_agent)
    app.include_router(router_users)
    app.include_router(router_pages)
    app.mount('/static', StaticFiles(directory='app/static'), name='static')
    yield
    await chroma_vectorstore.close()


app = FastAPI(lifespan=lifespan)
app.mount('/admin', admin_app)
