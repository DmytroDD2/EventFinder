from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from app.users.models import User
from app.events.models import Event


from typing import Optional

from app.tickets.models import Tickets
from app.tickets.schemas import BaseTicketCreate
from sqlalchemy.orm import joinedload

from app.notifications.models import Notification


def add_notification_edit_event(db, event: Event):
    if event.data:
        event_date = event.data.date()
        event_time = event.data.time()
    else:
        event_date = "not yet known"
        event_time = "not yet known"

    message = f'Change in event {event.name}.  Start date {event_date} at {event_time}. Location: {event.venue}'
    tickets = db.query(Tickets.id).filter(Tickets.event_id == event.id).all()
    notifications = [Notification(ticket_id=ticket_id[0], message=message) for ticket_id in tickets]
    db.add_all(notifications)
    db.commit()
    return


def add_notification(db, ticked_id: id, event: Event):
    if event.data:
        event_date = event.data.date()
        event_time = event.data.time()
    else:
        event_date = "not yet known"
        event_time = "not yet known"

    message = f'You are registered for the event: {event.name}.Start date{event_date} at {event_time}. Location: {event.venue}'
    db_notification = Notification(ticket_id=ticked_id, message=message)
    db.add(db_notification)
    db.commit()

    return db_notification


def get_all_notifications(db: Session, user_id: int):
    db_notification = (db.query(Notification).
                       join(Tickets).join(User).
                       filter(User.id == user_id).
                       order_by(asc(Notification.is_read), Notification.id).all())
    if not db_notification:
        raise HTTPException(status_code=204, detail="You don't have any messages")
    return db_notification


def get_notification_by_id(db: Session, notification_id: int, user_id: int):
    db_notification = (db.query(Notification).
                       join(Tickets).join(User).
                       filter(User.id == user_id, Notification.id == notification_id).first())

    if db_notification and not db_notification.is_read:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)

    return db_notification


def get_all_read_notifications(db: Session, user_id: int, read: bool):
    db_notification = (db.query(Notification).
                       join(Tickets).join(User).
                       filter(User.id == user_id, Notification.is_read == read).all())
    detail = "No messages have been read" if read else "Mark all messages as read"
    if not db_notification:
        raise HTTPException(status_code=404, detail=detail)

    return db_notification
