from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
    Response
)
import jwt
from jwt import PyJWTError

from app.config import get_auth_data
from app.exceptions import NoJwtException
from app.users.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
)
from app.users.dao import UsersDAO
from app.users.dependencies import (
    get_current_user,
    get_current_super_admin_user
)
from app.users.models import User
from app.users.schemas import (
    SchemaUserRegister,
    SchemaUserAuth,
    SchemaUserRead,
    SchemaUserDataUpdate,
    SchemaUserRoleUpdate
)
from app.users.service import UserService


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register/')
async def register_user(user_data: SchemaUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/', summary='Create Access Token and Refresh Token')
async def auth_user(response: Response, user_data: SchemaUserAuth):
    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password
        )
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({'sub': str(check.id)})
    refresh_token = create_refresh_token({'sub': str(check.id)})
    response.set_cookie(
        key='users_access_token',
        value=access_token,
        httponly=True
        )
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/refresh', summary='Refresh Token')
async def refresh_token(refresh_token: str = Body(...)):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(
            refresh_token,
            auth_data['jwt_refresh_secret_key'],
            auth_data['algorithm']
            )
        user_id = payload.get('sub')
        if user_id is None:
            raise NoJwtException
        new_token = create_access_token({'sub': str(user_id)})
        return {'access_token': new_token, 'token_type': 'Bearer'}

    except PyJWTError:
        raise NoJwtException


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'Вы успешно вышли из системы'}


@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.get('/me/update', response_model=SchemaUserRead)
async def update_me(
    user_data: User = Depends(get_current_user),
    data: SchemaUserDataUpdate = Depends(SchemaUserDataUpdate),
):
    updates = {}
    updates['dealer_code'] = data.dealer_code
    updates['email'] = data.email
    updates['phone_number'] = data.phone_number
    await UsersDAO.update(filter_by={'id': user_data.id}, **updates)
    user_updated = await UsersDAO.find_one_or_none_by_id(user_data.id)
    return user_updated


@router.get('/all_users/')
async def get_all_users(
    user_data: User = Depends(get_current_super_admin_user)
):
    return await UsersDAO.find_all()


@router.post('/user/{user_id}/update', response_model=SchemaUserRead)
async def update_user_role(
    user_id: int,
    data: SchemaUserRoleUpdate = Depends(SchemaUserRoleUpdate),
    user_role: User = Depends(get_current_super_admin_user),
):
    user_data = await UsersDAO.find_one_or_none_by_id(user_id)
    data = await UserService.update_user_role(data, user_data)
    return data


@router.get('/user/{user_id}', response_model=SchemaUserRead)
async def get_user(
    user_id: int,
    user_data: User = Depends(get_current_super_admin_user)
):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    data = UserService.get_user_dto(user)
    return data
