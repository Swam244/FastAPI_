from fastapi import Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from .. import models,schemas,utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    
    hash_pass = utils.hash(user.password)
    user.password = hash_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.UserGet])
def get_users(db : Session = Depends(get_db)):
    data = db.query(models.User).all()
    return data

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserResponse)
def get_user(id : int , db : Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found")
    return data