from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

@app.post("/posts", status_code=status.HTTP_201_CREATED) # add status code to the decorator for default values
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict} # return the data

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
    