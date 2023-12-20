from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from app.events.models import Event
from app.events.schemas import BaseEvent, BaseFilter, EventParams
from app.notifications.crud import add_notification_edit_event


def add_event(db: Session, event: BaseEvent, creator: int):
    db_event = Event(**event.model_dump(), creator=creator)
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


def change_event(db: Session, new_event: BaseEvent, old_event: Event):
    for key, value in new_event:
        if value not in ["string", None]:
            setattr(old_event, key, value)

    # old_event.name = new_event.name
    #
    # old_event.description = new_event.description
    # old_event.total_tickets = new_event.total_tickets

    db.commit()
    db.refresh(old_event)
    return old_event

def get_all_events(db, event_pars: EventParams):
    offset = (event_pars.page - 1) * event_pars.per_page
    db_events = db.query(Event).offset(offset).limit(event_pars.per_page).all()
    return db_events


def filter_event(db: Session, details: BaseFilter):
    query = db.query(Event)
    filters = []

    if details.start_date:
        filters.append(and_(Event.data >= details.start_date, Event.data <= details.end_date))

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

    if filters:
        offset = (details.page - 1) * details.per_page

        result = query.filter(and_(*filters)).offset(offset).limit(details.per_page).all()
        if result:
            return result

    raise HTTPException(status_code=404, detail="Event not found")











