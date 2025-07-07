from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func, true, and_
from sqlalchemy.orm import Session, joinedload, selectinload
from app.events.models import Event, EventImage
from app.events.schemas import BaseEvent, BaseFilter, EventParams, Category, BaseEventFirst
from app.notifications.crud import add_notification_edit_event
from datetime import date

from app.utils.file_operations import delete_file


def add_event(db: Session, event: BaseEvent, creator: int):
    if db.query(Event).filter(Event.name == event.name).first():
        raise HTTPException(
            status_code=409,
            detail=f"Event name '{event.name}'is already taken. Choose a different name.")


    db_event = Event(**event.model_dump(exclude={"images"}), creator=creator)
    if event.images:
        db_images = [EventImage(event_id=db_event.id, image_url=image) for image in event.images]
        db_event.images = db_images

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


def find_event(db: Session, event_id: int):
    db_event = db.get(Event, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


def del_event(db: Session, event: Event):

    db.delete(event)
    db.commit()
    return event


def change_event(db: Session, new_event: BaseEventFirst, old_event: Event):
    for key, value in new_event:
        if value and key != "images": # not in ["string", None]:
            setattr(old_event, key, value)


    if new_event.images:

        db_images = [EventImage(event_id=old_event.id, image_url=image) for image in new_event.images]
        db.add_all(db_images)
    db.commit()
    db.refresh(old_event)
    return old_event

def get_all_events(db, event_pars: EventParams):
    offset = (event_pars.page - 1) * event_pars.per_page
    db_events = (db.query(Event).options(joinedload(Event.images))
                 .filter(
                     or_(
                         Event.data == None,
                         Event.data > date.today())
                 )
                 .offset(offset).limit(event_pars.per_page).all())
    return db_events

def get_my_event(db, event_pars: EventParams, my_id: int):
    offset = (event_pars.page - 1) * event_pars.per_page
    db_event = db.query(Event).options(selectinload(Event.images)) .filter(Event.creator == my_id).offset(offset).limit(event_pars.per_page).all()
    return db_event

def remove_event_image(db, image_id: int, event_id: int):
    image = db.query(EventImage).filter(EventImage.id == image_id, EventImage.event_id == event_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image_name = image.image_url
    db.delete(image)
    db.commit()
    delete_file(image_name)

    return {"message": "Image deleted successfully"}


def append_user_image(db, event_id: int, images: list):

    db_images = [EventImage(event_id=event_id, image_url=image) for image in images]

    db.add_all(db_images)
    db.commit()
    # db.refresh(db_images)


def filter_event(db: Session, details: BaseFilter):

    query = db.query(Event).options(selectinload(Event.images))
    filters = []

    if details.start_date:
        filters.append(Event.data >= details.start_date)

    if details.end_date:
        filters.append(func.date(Event.data) <= details.end_date)

    if details.location:
        filters.append(Event.venue == details.location)

    if details.category:
        filters.append(Event.category == details.category)

    if details.search_term:
        filters.append(or_(Event.name.ilike(f"%{details.search_term}%"),
                           Event.description.ilike(f"%{details.search_term}%")))

    if details.min_price is not None:
        filters.append(Event.price >= details.min_price)

    if details.max_price is not None:
        filters.append(Event.price <= details.max_price)
    offset = (details.page - 1) * details.per_page


    if filters:
        if not details.start_date:
            filters.append(Event.data > date.today())

            print(date.today(), Event.data, "*" * 100)
        result = query.filter(and_(*filters)).offset(offset).limit(details.per_page).all()

        result = {"items": result}

        if details.totalCount:
            effective_filters = filters if filters else [true()]
            total_count = query.filter(and_(*effective_filters)).count()
            result["totalCount"] = total_count



        return result
        # if details.include_total:
        #     result.totalCount = query.count()
        # if result:
        #     return result
    else:
        result = {"items": get_all_events(db, EventParams(per_page=details.per_page, page=details.page))}
        if details.totalCount:
            total_count = query.count()
            result["totalCount"] = total_count


        return result

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    # raise HTTPException(status_code=404, detail="Event not found")











