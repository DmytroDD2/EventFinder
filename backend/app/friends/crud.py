from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.users.models import User
from app.friends.models import Friendship
from app.users.crud import find_user

router = APIRouter()

def add_friendship(db, user_id: int, friend_id: int):
    friend_user = db.query(User).filter(User.id == friend_id).first()

    if not friend_user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"User with ID {friend_id} not found"
        )

    friendship = Friendship(user_id=user_id, friend_id=friend_id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


def remove_friendship(db, user_id: int, friend_id: int):
    friendship = db.query(Friendship).filter(
        Friendship.user_id == user_id,
        Friendship.friend_id == friend_id
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    db.delete(friendship)
    db.commit()
    return True

def get_friends(db: Session, user_id: int):
    friends = db.query(User).join(Friendship, and_(User.id == Friendship.friend_id)).filter(Friendship.user_id == user_id).all()
    print("")
    if not friends:
        raise HTTPException(status_code=204, detail="User has no friends")
    return friends
