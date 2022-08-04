from fastapi import FastAPI,Request,APIRouter,Depends,status,HTTPException,WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

router=APIRouter(tags=['home'])
templates=Jinja2Templates(directory="templates")

@router.get('/')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/login')
def login(request:Request):
    return templates.TemplateResponse('login.html', {'request':request})

@router.get('/register')
def register(request:Request):
    return templates.TemplateResponse('register.html', {'request':request})

