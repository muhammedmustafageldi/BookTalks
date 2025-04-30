from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["Auth HTML"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/login-page", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get("/register-page", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})