from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''Select * from posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # add status code to the decorator for default values
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): # Get current user dependecy to restric access
    # DO NOT USE FSTRINGS: they make us vulnerable to SQL Injection attacks
    # cursor.execute("""Insert into posts (title, content, published, owner_id) values (%s, %s, %s, 11) returning * """,(post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.dict()) Dictionary unpacking
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) # Add the new post to commit
    db.commit() # Commit the new post
    db.refresh(new_post) # Retrieve the new post and save it to the variable again

    return new_post # return the data

@router.get("/{id}", response_model=schemas.Post) # path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''Select * from posts where id = %s ''', (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!!"}

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting post
    # cursor.execute("""Delete from posts where id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested action!")

    post_query.delete(synchronize_session = False)
    db.commit()

    # We do not return a message!
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Put method requires all the fields to be sent again
# whereas the patch method requires for only the changed ones
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("update posts set title = %s, content = %s, published = %s, owner_id = 11 where id = %s returning *",
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exists!!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested action!")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()