from fastapi import FastAPI
from database import engine,get_db
from fastapi.staticfiles import StaticFiles
from routes import home,auth
import models

app=FastAPI()
app.mount('/static',StaticFiles(directory="static"),name="static")
models.Base.metadata.create_all(engine)

app.include_router(home.router)
app.include_router(auth.router)

