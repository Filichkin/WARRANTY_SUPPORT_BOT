from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.users.dao import UsersDAO
from app.users.dependencies import get_optional_current_user


router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/auth/register/', response_class=HTMLResponse)
async def registration_page(
    request: Request
):
    user = await UsersDAO.find_one_or_none(email=request.get('email'))
    if user:
        return templates.TemplateResponse(
            'login.html',
            {'request': request}
            )
    else:
        return templates.TemplateResponse(
            'registration.html',
            {'request': request}
            )


@router.get('/auth/login/', response_class=HTMLResponse)
async def login_page(
    request: Request,
    user: int = Depends(get_optional_current_user),
):
    if user:
        return RedirectResponse(url='/')
    else:
        return templates.TemplateResponse('login.html', {'request': request})


@router.get('/', response_class=HTMLResponse)
async def chat_page(
    request: Request,
    user: int = Depends(get_optional_current_user),
):
    if user:
        return templates.TemplateResponse('index.html', {'request': request})
    else:
        return RedirectResponse(url='/auth/login/')
