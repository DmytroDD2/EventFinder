from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Header, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.main import app
from app.reviews.schemas import BaseReview, ReviewParams, ResponseUserReview, ResponseEventReviews
from app.users.schemas import UserToken, Role
from app.users.security import get_current_user_token
from app.reviews.crud import add_review, get_review_for_event, del_review, find_review, get_user_review
from app.events.crud import find_event

from celery_worker import send_email_task

router = APIRouter()


@router.post("/event/{event_id}/create-review", response_model=BaseReview, status_code=status.HTTP_201_CREATED)
async def create_review(review: BaseReview,
                       event_id: int,
                       db: Session = Depends(get_db),
                       user: UserToken = Depends(get_current_user_token)):

    db_event = add_review(db, review, user.id, event_id)
    return db_event


@router.get("/event/{event_id}/",response_model=List[ResponseEventReviews], status_code=200)
async def get_all_review(
        event_id: int,
        page: int = 1,
        per_page: int = 10,
        db: Session = Depends(get_db)
):

    all_review = get_review_for_event(db, event_id, page, per_page)

    return all_review


@router.get("/my",response_model=List[ResponseUserReview], status_code=200)
async def get_my_review(
        review_params: ReviewParams = Depends(),
        user: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    all_review = get_user_review(db, review_params, user.id)

    return all_review


@router.delete("/{review_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int,
                 user: UserToken = Depends(get_current_user_token),
                 db: Session = Depends(get_db)):

    review_exist = find_review(db, review_id)

    if review_exist.user_id != user.id and user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return del_review(db, review_exist)
