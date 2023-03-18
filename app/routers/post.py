from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from .. import models, schema, authentication
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schema.PostOut])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(authentication.get_current_user,),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(
    post: schema.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(authentication.get_current_user), 
    limit: int = 10
):
    print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(authentication.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post wid id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(authentication.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requestet action')
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(authentication.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    pdated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
  
    return post_query.first()



