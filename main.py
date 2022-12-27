from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Pydantic model to validate the data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None # Optional Field Defaults to None

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
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # return the data

@app.get("/posts/{id}") # path parameter
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_details": post}