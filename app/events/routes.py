import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Header, Form
from sqlalchemy.orm import Session
from app.events.schemas import BaseEvent, EventResponse, BaseFilter, Category, EventParams, ResponseEvent
from app.db.session import get_db

from app.users.security import oauth2_scheme, get_current_user_token, permission

from app.users.schemas import UserToken
from app.notifications.crud import add_notification_edit_event

from .crud import add_event, del_event, find_event, change_event, get_all_events, filter_event, get_my_event

router = APIRouter()


@router.get("", response_model=list[EventResponse], status_code=200)
async def get_all_event(db: Session = Depends(get_db), event_pars: EventParams = Depends()):
    return get_all_events(db, event_pars)


@router.get("/my", response_model=list[EventResponse], status_code=200)
async def get_all_event(db: Session = Depends(get_db),
                        event_pars: EventParams = Depends(),
                        user: UserToken = Depends(get_current_user_token)):
    return get_my_event(db, event_pars, user.id)


@router.get("/filter", response_model=list[ResponseEvent], status_code=200)
async def get_filter_event(
        details: BaseFilter = Depends(),
        db: Session = Depends(get_db)):
    return filter_event(db, details)


@router.post("/create-event", response_model=BaseEvent, status_code=status.HTTP_201_CREATED)
async def create_event(event: BaseEvent,
                       db: Session = Depends(get_db),
                       creator: UserToken = Depends(get_current_user_token)):
    db_event = add_event(db, event, creator.id)

    return db_event


@router.delete("/{event_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int,
                 creator: UserToken = Depends(get_current_user_token),
                 db: Session = Depends(get_db)):

    event_exist = find_event(db, event_id)

    if event_exist.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return del_event(db, event_exist)


@router.put("/{event_id}/edit", response_model=BaseEvent, status_code=status.HTTP_200_OK)
def edit_event(
    event_id: int,
    edited_event: BaseEvent,
    creator: UserToken = Depends(get_current_user_token),
    db: Session = Depends(get_db)
):

    event = find_event(db, event_id)

    if event.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    event_chen = change_event(db, edited_event, event)
    add_notification_edit_event(db, event_chen)
    return event_chen
