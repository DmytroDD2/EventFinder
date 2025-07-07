

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.events.models import Event, EventImage
from app.reviews.models import Review
from app.reviews.schemas import BaseReview, ReviewParams
from app.events.crud import find_event
from app.users.crud import find_user
from app.users.models import User


def add_review(db: Session, review: BaseReview, user: int, event_id: int):
    db_review = Review(**review.model_dump(), user_id=user, event_id=event_id)

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review_for_event(db: Session, event_id: int, page: int = 1, per_page: int = 10):
    event_exist = find_event(db, event_id)

    offset = (page - 1) * per_page

    results = db.query(
        Review.id,
        Review.rating,
        Review.description,
        Review.user_id,
        Review.event_id,

        User.profile_picture.label("image_url"),
        User.username.label("name")
    ).join(
        User, User.id == Review.user_id
    ).filter(
        Review.event_id == event_id
    ).offset(offset).limit(per_page).all()

    return results

def get_user_review(db: Session, params: ReviewParams, user_id: int):
    offset = (params.page - 1) * params.per_page

    user = find_user(db, user_id)

    subquery = (
        db.query(
            EventImage.event_id,
            EventImage.image_url,
            Event.name
        ).join(Event, Event.id == EventImage.event_id)
        .distinct(EventImage.event_id)
        .subquery()
    )

    query = (
        db.query(
            Review.id,
            Review.rating,
            Review.description,
            Review.user_id,
            Review.event_id,
            subquery.c.image_url,
            subquery.c.name
        )
        .outerjoin(subquery, Review.event_id == subquery.c.event_id)
        .filter(Review.user_id == user_id)
        .offset(offset)
        .limit(params.per_page)
    )

    results = query.all()

    return results


def find_review(db: Session, review_int: int):
    db_review = db.query(Review).filter(Review.id == review_int).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="review not found")
    return db_review


def del_review(db: Session, review: Review):
    db.delete(review)
    db.commit()
    return review

