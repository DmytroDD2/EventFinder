from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users.models import User
from app.events.models import Event
from app.events.schemas import BaseEvent
from typing import Optional
from datetime import date, time
from app.tickets.models import Tickets
from app.tickets.schemas import BaseTicketCreate
from sqlalchemy.orm import joinedload

from app.events.crud import find_event
from app.users.crud import find_user


def add_ticket(db, event: Event, user: User):
    db_ticket = Tickets(event_id=event.id, user_id=user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    event.total_tickets -= 1
    db.commit()

    user.balance -= event.price
    db.commit()

    return db_ticket


def get_user_tickets(db, user_id: int):
    user_tickets = db.query(
        Event.name.label("event_name"),
        User.username.label("user_name"),
        Event.data.label("data"),
        User.username.label("creator"),
        Event.description.label("description"),
        Event.price.label("price"),
        Tickets.id.label("ticket_id"),
    ).\
        join(Event, Tickets.event_id == Event.id).\
        join(User, Tickets.user_id == User.id). \
        filter(User.id == user_id). \
        all()
    if user_tickets is None:
        raise HTTPException(status_code=404, detail="You don`t have tickets yet")
    return user_tickets


def find_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


def del_ticket(db: Session, ticket: Tickets, event_id: int):
    db.delete(ticket)
    db.commit()

    event = db.query(Event).filter(Event.id == event_id).first()
    event.total_tickets += 1
    db.commit()
    return

def get_all_ticket(db: Session):  #Not is use now
    db_ticket = db.query(Tickets).all()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="You don`t have tickets yet")
    return db_ticket




def validate_purchase(db: Session, event_id: int, user_id: int):

    event = find_event(db, event_id)
    user = find_user(db, user_id)

    if not event or not user:
        raise HTTPException(status_code=404, detail="Event or User not found")

    tickets = db.query(Tickets).filter(Tickets.event_id == event_id).filter(Tickets.user_id == user_id).all()

    if tickets:
        raise HTTPException(status_code=400, detail="User already purchased a ticket for this event")

    if event.total_tickets < 1:
        raise HTTPException(status_code=403, detail="Tickets are sold out")

    if user.balance < event.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    return event, user


