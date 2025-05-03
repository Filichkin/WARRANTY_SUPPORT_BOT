from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import (
    ShchemaUserRoleUpdate,
    SchemaUserRead
)


class UserService:
    @staticmethod
    def get_user_dto(user_data: User):
        return SchemaUserRead(
            id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_user=user_data.is_user,
            is_employe=user_data.is_super_admin,
        )

    @staticmethod
    async def update_user_role(data: ShchemaUserRoleUpdate, user: User):
        updates = {}
        if data.is_super_admin:
            updates['is_super_admin'] = data.is_super_admin
        if updates:
            await UsersDAO.update(filter_by={'id': user.id}, **updates)

        user_updated = await UsersDAO.find_one_or_none_by_id(user.id)
        return user_updated
