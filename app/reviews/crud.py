from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.reviews.models import Review
from app.reviews.schemas import BaseReview
from app.events.crud import find_event


def add_review(db: Session, review: BaseReview, user: int, event_id: int):
    db_review = Review(**review.model_dump(), user_id=user, event_id=event_id)

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review_for_event(db: Session, event_id: int, page: int = 1, per_page: int = 10):
    event_exist = find_event(db, event_id)

    offset = (page - 1) * per_page

    return event_exist, db.query(Review).filter(Review.event_id == event_id).offset(offset).limit(per_page).all()


def find_review(db: Session, review_int: int):
    db_review = db.query(Review).filter(Review.id == review_int).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="review not found")
    return db_review


def del_review(db: Session, review: Review):
    db.delete(review)
    db.commit()
    return review

