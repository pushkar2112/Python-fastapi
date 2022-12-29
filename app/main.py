from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Pydantic model to validate the data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None # Optional Field Defaults to None

# DB Connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='<PASSWORD>', cursor_factory=RealDictCursor)
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

@app.get("/posts")
def get_posts():
    cursor.execute('''Select * from posts''')
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # add status code to the decorator for default values
def create_posts(post: Post):
    # DO NOT USE FSTRINGS: they make us vulnerable to SQL Injection attacks
    cursor.execute("""Insert into posts (title, content, published, owner_id) values (%s, %s, %s, 11) returning * """,(post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post} # return the data

@app.get("/posts/{id}") # path parameter
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!!"}

    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, response: Response):
    #deleting post
    try:
        post_index = my_posts.index(find_post(id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")
    
    del my_posts[post_index]
# We do not return a message!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Put method requires all the fields to be sent again
# whereas the patch method requires for only the changed ones
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    try:
        post_index = my_posts.index(find_post(id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[post_index] = post_dict
    return {'data': post_dict}
    