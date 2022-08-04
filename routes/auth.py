from fastapi import FastAPI,Request,APIRouter,Depends,status,HTTPException,Form,status,Response,WebSocket
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi_login.exceptions import InvalidCredentialsException
import database,models
from hashing import Hash
import os
from fastapi_login import LoginManager



router=APIRouter(tags=['auth'])
templates=Jinja2Templates(directory="templates")


SECRET=os.urandom(24).hex()
manager=LoginManager(SECRET, token_url='/login',use_cookie=True)
manager.cookie_name="bearer"


@manager.user_loader
def load_user(email:str):
    db=next(database.get_db())
    user=db.query(models.User).filter(models.User.email==email).first()
    return user


@router.post('/register')
async def register(request:Request,email: str = Form(),password: str = Form(),name: str = Form(),db:Session=Depends(database.get_db)):
    new_user=models.User(name=name,email=email,password=Hash.bcrypt(password))

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    resp=RedirectResponse(url="login",status_code=status.HTTP_302_FOUND)

    return resp

@router.post('/login')
def login(email: str = Form(),password: str = Form()):

    user=load_user(email)

    if not user:
        raise InvalidCredentialsException

    if not Hash.verify(user.password,password):
        raise InvalidCredentialsException
    
    access_token=manager.create_access_token(data={"sub":email})

    resp=RedirectResponse(url="/message",status_code=status.HTTP_302_FOUND)

    manager.set_cookie(resp, access_token)

    return resp


@router.get('/logout')
def logout(response : Response):
  response = RedirectResponse('/login', status_code= 302)
  manager.set_cookie(response, "")
  return response


@router.get('/message')
def messageHome(request:Request,_=Depends(manager)):
    return  templates.TemplateResponse('messages.html', {'request':request})


websocket_list=[]
@router.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()

    # current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

    # print(current_active_verified_user)

    if websocket not in websocket_list:
        websocket_list.append(websocket)
    
    while True:
        data=await websocket.receive_text()
        for web in websocket_list:
            if web!=websocket:
                await web.send_text(f"{data}")