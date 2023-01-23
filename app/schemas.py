import imp
from pydantic import BaseModel

# Pydantic model to validate the data
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
