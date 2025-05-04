from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.users.dependencies import get_optional_current_user


router = APIRouter()

templates = Jinja2Templates(directory='app/templates')


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
