"""
auto_create_notifications.py

This script is designed to automatically create notifications for upcoming events.
It queries the database for events scheduled for tomorrow and generates notifications accordingly.

Usage:
  python auto_create_notifications.py
"""



import sys
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]


sys.path.append(str(project_root))
from app.users.models import User
from app.db.session import get_db
from app.events.models import Event
from app.notifications.models import Notification
from app.tickets.models import Tickets

router = APIRouter()

def create_notifications_for_upcoming_events(db: Session = Depends(get_db), days_before: int = 1):

    target_date = datetime.now().date() + timedelta(days=days_before)
    upcoming_events= (db.query(Tickets.id, Event.name, Event.data).join(Event).
                      filter(Event.data >= target_date, Event.data < target_date + timedelta(days=1), Event.data.isnot(None)).all())
    for ticket_id, event_name, event_date in upcoming_events:
        formatted_date = event_date.strftime("%Y-%m-%d")
        formatted_time = event_date.strftime("%H:%M:%S")
        message = f'Tomorrow is the day of the event {event_name},  {formatted_date} at {formatted_time}'
        notification = Notification(ticket_id=ticket_id, message=message)
        db.add(notification)

    db.commit()
    return


if __name__ == "__main__":
    db = next(get_db())
    create_notifications_for_upcoming_events(db)