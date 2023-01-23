from turtle import title
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic model to validate the data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data" : posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''Select * from posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # add status code to the decorator for default values
def create_posts(post: Post, db: Session = Depends(get_db)):
    # DO NOT USE FSTRINGS: they make us vulnerable to SQL Injection attacks
    # cursor.execute("""Insert into posts (title, content, published, owner_id) values (%s, %s, %s, 11) returning * """,(post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.dict()) Dictionary unpacking
    new_post = models.Post(**post.dict())
    db.add(new_post) # Add the new post to commit
    db.commit() # Commit the new post
    db.refresh(new_post) # Retrieve the new post and save it to the variable again

    return {"data": new_post} # return the data

@app.get("/posts/{id}") # path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute('''Select * from posts where id = %s ''', (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!!"}

    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, response: Response, db: Session = Depends(get_db)):
    #deleting post
    # cursor.execute("""Delete from posts where id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    post.delete(synchronize_session = False)
    db.commit()

    # We do not return a message!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Put method requires all the fields to be sent again
# whereas the patch method requires for only the changed ones
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    
    # cursor.execute("update posts set title = %s, content = %s, published = %s, owner_id = 11 where id = %s returning *",
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return {'data': post_query.first()}
    