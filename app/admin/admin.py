from fastadmin import register, SqlAlchemyModelAdmin

from app.database import async_session_maker
from app.users.auth import verify_password
from app.users.dao import UsersDAO
from app.users.models import User


@register(User, sqlalchemy_sessionmaker=async_session_maker)
class UserAdmin(SqlAlchemyModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_super_admin')
    list_display_links = ('id', 'email')

    async def authenticate(self, email, password):
        user = await UsersDAO.find_one_or_none(email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        print(user.id)
        return user.id
