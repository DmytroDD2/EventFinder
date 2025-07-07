import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Header, Form, UploadFile, File, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from app.events.schemas import BaseEvent, BaseFilter, Category, EventParams, ResponseEvent, BaseEventFirst, \
    BaseEventEdit, ResponseSingleEvent, PaginatedEvents, ResponseMyEvent
from app.db.session import get_db

from app.users.security import get_current_user_token, permission

from app.users.schemas import UserToken
from app.notifications.crud import add_notification_edit_event

from .crud import add_event, del_event, find_event, change_event, get_all_events, filter_event, get_my_event, \
    remove_event_image, append_user_image
from ..utils.file_operations import save_file

router = APIRouter()


@router.get("", response_model=list[ResponseEvent], status_code=200)
async def get_all_event(
        db: Session = Depends(get_db),
        event_pars: EventParams = Depends()
):
    return get_all_events(db, event_pars)


@router.get("/my", response_model=list[ResponseMyEvent], status_code=200)
async def get_all_event(
        db: Session = Depends(get_db),
        event_pars: EventParams = Depends(),
        user: UserToken = Depends(get_current_user_token)
):
    return get_my_event(db, event_pars, user.id)

@router.get("/admin/user/{user_id}", response_model=list[ResponseEvent], status_code=200)
async def get_some_user_event(
        user_id: int,
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token),
        event_pars: EventParams = Depends()
):
    permission(admin)
    events = get_my_event(db, event_pars, user_id)

    return events

@router.get("/filter", response_model=PaginatedEvents, status_code=200)
async def get_filter_event(
        details: BaseFilter = FilterDepends(BaseFilter),
        db: Session = Depends(get_db)):

    return filter_event(db, details)


@router.post("/create-event", response_model=ResponseEvent, status_code=status.HTTP_201_CREATED)
async def create_event(
        event: BaseEvent = Depends(),
        db: Session = Depends(get_db),
        creator: UserToken = Depends(get_current_user_token)
):


    if event.images:
        event.images = [await save_file(image) for image in event.images]

    db_event = add_event(db, event, creator.id)

    return db_event

@router.post("/admin/user/{user_id}/create-event", response_model=ResponseEvent, status_code=status.HTTP_201_CREATED)
async def create_event_for_user(
        user_id: int,
        event: BaseEvent = Depends(),
        db: Session = Depends(get_db),
        creator: UserToken = Depends(get_current_user_token)
):
    permission(creator)

    if event.images:
        event.images = [await save_file(image) for image in event.images]

    db_event = add_event(db, event, user_id)

    return db_event

@router.get("/{event_id}", response_model=ResponseSingleEvent, status_code=status.HTTP_200_OK)
async def get_event(
        event_id: int,
        db: Session = Depends(get_db)
):
    return find_event(db, event_id)


@router.delete("/{event_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
        event_id: int,
        creator: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    event_exist = find_event(db, event_id)

    if event_exist.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return del_event(db, event_exist)


@router.put("/{event_id}/edit", response_model=ResponseEvent, status_code=status.HTTP_200_OK)
async def edit_event(
    edited_event: BaseEventEdit = Depends(),
    creator: UserToken = Depends(get_current_user_token),
    db: Session = Depends(get_db)
):

    event = find_event(db, edited_event.event_id)

    if event.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")


    if edited_event.images:
        edited_event.images = [await save_file(image) for image in edited_event.images]

    event_chen = change_event(db, edited_event, event)

    add_notification_edit_event(db, event_chen)
    return event_chen


@router.delete("/{event_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_image(
        event_id: int,
        image_id: int,
        creator: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):

    event_exist = find_event(db, event_id)

    if event_exist.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return remove_event_image(db, event_id=event_id, image_id=image_id)



@router.post("/events/{event_id}/images/",  response_model=ResponseEvent)
async def add_event_image(
        event_id: int,
        images: List[UploadFile]= File(...),
        creator: UserToken = Depends(get_current_user_token),
        db: Session = Depends(get_db)
):
    event_exist = find_event(db, event_id)
    if event_exist.creator != creator.id and not permission(creator):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    images = [ await save_file(image) for image in images]

    append_user_image(db, event_id, images)

    return  event_exist