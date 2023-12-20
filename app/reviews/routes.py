
from fastapi import APIRouter, Depends, HTTPException, status, Header, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.reviews.schemas import BaseReview
from app.users.schemas import UserToken
from app.users.security import get_current_user_token
from app.reviews.crud import add_review, get_review_for_event, del_review, find_review
from app.events.crud import find_event

router = APIRouter()


@router.post("/create-review", response_model=BaseReview, status_code=status.HTTP_201_CREATED)
async def create_event(review: BaseReview,
                       event_id: int,
                       db: Session = Depends(get_db),
                       user: UserToken = Depends(get_current_user_token)):

    db_event = add_review(db, review, user.id, event_id)
    return db_event


@router.get("", status_code=200)
async def get_all_review(event_id: int, page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):

    all_review = get_review_for_event(db, event_id, page, per_page)

    return all_review


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(review_id: int,
                 user: UserToken = Depends(get_current_user_token),
                 db: Session = Depends(get_db)):

    review_exist = find_review(db, review_id)

    if review_exist.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return del_review(db, review_exist)
