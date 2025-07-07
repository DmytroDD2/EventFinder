from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.users.schemas import UserToken
from app.users.security import get_current_user_token, permission
from app.friends.crud import get_friends, add_friendship, remove_friendship
from app.friends.schemas import BaseUserFriend

router = APIRouter()

@router.get("", response_model=list[BaseUserFriend])
async def get_user_friends(db: Session = Depends(get_db),
                           user: UserToken = Depends(get_current_user_token)):

    return get_friends(db, user.id)


@router.get("/{user_id}", response_model=list[BaseUserFriend])
async def get_some_user_friends(
                            user_id: int,
                           db: Session = Depends(get_db),
                           user: UserToken = Depends(get_current_user_token)):
    permission(user)
    print("=" * 20)
    return get_friends(db, user_id)



@router.post("/{friend_id}/add", status_code=status.HTTP_201_CREATED)
async def add_friend(friend_id: int,
                     db: Session = Depends(get_db),
                     user: UserToken = Depends(get_current_user_token)):
    friend = add_friendship(db, user.id, friend_id)

    if not friend:
        raise HTTPException(status_code=400, detail="Could not add friend")
    return friend


@router.post("/admin/{user_id}/{friend_id}/add", status_code=status.HTTP_201_CREATED)
async def add_friend(friend_id: int,
                     user_id:int,
                     db: Session = Depends(get_db),
                     user: UserToken = Depends(get_current_user_token)):
    friend = add_friendship(db, user_id, friend_id)
    permission(user)
    if not friend:
        raise HTTPException(status_code=400, detail="Could not add friend")
    return friend

@router.delete("/{friend_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(friend_id: int,
                        db: Session = Depends(get_db),
                        user: UserToken = Depends(get_current_user_token)):
    success = remove_friendship(db, user.id, friend_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not remove friend")


@router.delete("/admin/{user_id}/{friend_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend_admin(friend_id: int,
                              user_id: int,
                              db: Session = Depends(get_db),
                              user: UserToken = Depends(get_current_user_token)):
    permission(user)
    success = remove_friendship(db, user_id, friend_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not remove friend")