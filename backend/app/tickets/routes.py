from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.events.crud import find_event
from app.tickets.crud import add_ticket, get_user_tickets, find_ticket, del_ticket, get_all_ticket, validate_purchase, \
    get_friend_tickets
from app.tickets.schemas import BaseTicketCreate, BaseTicketCreate2, BaseResponseTickets, BaseResponseFriendsTickets
from app.users.security import get_current_user_token, permission
from app.tickets.models import Tickets
from app.users.schemas import UserToken
from app.notifications.crud import add_notification
from app.users.crud import find_user

router = APIRouter()


@router.get("", response_model=list[BaseResponseTickets],status_code=200)
async def get_all_user_ticket(
    db: Session = Depends(get_db),
    user: UserToken = Depends(get_current_user_token
)):
    tickets_us = get_user_tickets(db, user.id)

    return tickets_us


@router.get("/admin/{user_id}", response_model=list[BaseResponseTickets], status_code=200)
async def get_some_user_tickets(
        user_id: int,
        db: Session = Depends(get_db),
        admin: UserToken = Depends(get_current_user_token)
):

    permission(admin)
    tickets = get_user_tickets(db, user_id)

    return tickets


@router.get("/friends", response_model=list[BaseResponseFriendsTickets], status_code=200)
async def get_all_friend_tickets(
        db: Session = Depends(get_db),
        user: UserToken = Depends(get_current_user_token)
):
    return get_friend_tickets(db, user.id)


@router.post("/{event_id}/reserve",  response_model=BaseTicketCreate, status_code=201)
async def create_tickets(
        event_id: int,
        db: Session = Depends(get_db),
        user_client: UserToken = Depends(get_current_user_token)
):


    event, user = validate_purchase(db, event_id, user_client.id)

    db_ticket = add_ticket(db, event, user)
    add_notification(db, db_ticket.id, event)

    return {
        "creator": event.created_by.username,
        "data": event.data,
        "event_name": event.name,
        "user_name": db_ticket.user.username,
        "description": event.description,
        "ticket_id": db_ticket.id,
        "price": event.price
    }


@router.delete("/{ticket_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
        ticket_id: int,
        db: Session = Depends(get_db),
        user: UserToken = Depends(get_current_user_token)
):

    ticket_exist = find_ticket(db, ticket_id)

    if ticket_exist.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return del_ticket(db, ticket_exist, ticket_exist.event_id)










