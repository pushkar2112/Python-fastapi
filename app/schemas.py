from pydantic import BaseModel
from datetime import datetime

# Pydantic model to validate the data
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True # Used to return the data as a dict
