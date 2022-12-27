from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

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

# Api routes
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
# import Body to fetch the data from the request body
def create_posts(post: Post): # ... means that the data is required to be passed
    print(post)
    print(post.dict())
    return {"data": post} # return the data
# title str, content str