from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB Connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Pushkar1', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print("Connection failed!")
        print('ERROR: ', error)
        time.sleep(2)

# Temporary post storage
my_posts = [
    {"title": "title of post1", "content": "content of post1", "id": 1},
    {"title": "title of post2", "content": "content of post2", "id": 2}
    ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# Api routes
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

    
