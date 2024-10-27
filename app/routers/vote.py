from fastapi import Depends,APIRouter
from fastapi import status, HTTPException, Response
from ..schemas import Vote
from .. import models,database
from . import oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db : Session = Depends(database.get_db), user_id : int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id , models.Votes.user_id == user_id.id)
    found_vote = vote_query.first()
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user_id.id} has already voted on the post with id {vote.post_id}"
            )
        else:
            new_vote = models.Votes(post_id = vote.post_id, user_id = user_id.id)
            db.add(new_vote)
            db.commit()
            return {"Message":"Vote Added Successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Vote does not Exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()   
        
        return {"Message":"Successfully Deleted Vote"}