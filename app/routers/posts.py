from fastapi import Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status, HTTPException, Response
from .. import models,schemas
from ..database import engine,get_db
from . import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user),
              limit : int = 10,skip : int = 0,search : Optional[str]=""):
    
    data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,
            models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results


@router.get("/{id}", status_code=status.HTTP_200_OK,response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    
    # data = db.query(models.Post).filter(models.Post.id == id).first()
    
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,
            models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="POST WITH id = {} WAS NOT FOUND ".format(str(id)))

    return results


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def post_posts(
           post: schemas.PostCreate, 
           db: Session = Depends(get_db),
           user_id : int = Depends(oauth2.get_current_user)
            ):
    
    print(user_id)
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="POST WITH id = {} DOES NOT EXIST".format(str(id)))
        
    if deleted_post.first().owner_id != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform this action"    
        )
        
    deleted_post.delete(synchronize_session = False) 
    db.commit()   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id :int , post : schemas.PostCreate, db : Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post1 = post_query.first()
    if post1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist") 
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
