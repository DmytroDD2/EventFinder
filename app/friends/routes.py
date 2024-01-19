from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.users.schemas import UserToken
from app.users.security import get_current_user_token
from app.friends.crud import get_friends, add_friendship, remove_friendship
from app.friends.schemas import BaseUserFriend

router = APIRouter()

@router.get("/friends", response_model=list[BaseUserFriend])
async def get_user_friends(db: Session = Depends(get_db),
                           user: UserToken = Depends(get_current_user_token)):
    return get_friends(db, user.id)

@router.post("/friends/{friend_id}/add", status_code=status.HTTP_201_CREATED)
async def add_friend(friend_id: int,
                     db: Session = Depends(get_db),
                     user: UserToken = Depends(get_current_user_token)):
    friend = add_friendship(db, user.id, friend_id)

    if not friend:
        raise HTTPException(status_code=400, detail="Could not add friend")
    return friend

@router.delete("/friends/{friend_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(friend_id: int,
                        db: Session = Depends(get_db),
                        user: UserToken = Depends(get_current_user_token)):
    success = remove_friendship(db, user.id, friend_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not remove friend")
