from app.users.auth import get_password_hash, verify_password
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import (
    SchemaUserPasswordUpdate,
    SchemaUserRoleUpdate,
    SchemaUserRead
)


class UserService:
    @staticmethod
    def get_user_dto(user_data: User):
        return SchemaUserRead(
            id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            dealer_code=user_data.dealer_code,
            is_user=user_data.is_user,
            is_super_admin=user_data.is_super_admin,
        )

    @staticmethod
    async def update_user_role(data: SchemaUserRoleUpdate, user: User):
        updates = {}
        if data.is_super_admin:
            updates['is_super_admin'] = True
            updates['is_user'] = False
        if not data.is_super_admin:
            updates['is_super_admin'] = False
            updates['is_user'] = True
        if updates:
            await UsersDAO.update(filter_by={'id': user.id}, **updates)

        user_updated = await UsersDAO.find_one_or_none_by_id(user.id)
        return user_updated

    @staticmethod
    async def update_user_password(data: SchemaUserPasswordUpdate, user: User):
        updates = {}
        if (
            verify_password(
                plain_password=data.old_password,
                hashed_password=user.password
                )
            and data.new_password
        ):
            updates['password'] = get_password_hash(data.new_password)
        if updates:
            await UsersDAO.update(filter_by={'id': user.id}, **updates)

        user_updated = await UsersDAO.find_one_or_none_by_id(user.id)
        return user_updated
