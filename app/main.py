from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import SessionLocal, engine,get_db
from . import models,schemas,utils
from sqlalchemy.orm import session
from .routers import post,user,login

import time
app=FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
@app.get("/")
async def root():
 return {"message": "Hello learners!!!!!!!"}
