from fastadmin import register, SqlAlchemyModelAdmin
from fastadmin import fastapi_app as admin_app

from app.database import async_session_maker
from app.users.auth import verify_password
from app.users.dao import UsersDAO
from app.users.models import User


@register(User, sqlalchemy_sessionmaker=async_session_maker)
class UserAdmin(SqlAlchemyModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'dealer_code',
        'is_user',
        'is_super_admin',
        'created_at'
        )
    list_display_links = ('id',)

    async def authenticate(self, email, password):
        user = await UsersDAO.find_one_or_none(
            email=email,
            is_super_admin=True
            )
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user.id
