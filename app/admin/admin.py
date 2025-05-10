from fastadmin import fastapi_app as admin_app
from fastadmin import register, SqlAlchemyModelAdmin
from sqlalchemy import select

from app.database import async_session_maker
from app.users.models import User


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
            user = result.first()
            if not user:
                return None
            return user.id
