from contextlib import contextmanager
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy import inspect
from sqlalchemy.orm import Session
import random
from faker import Faker

from app.db import SessionLocal
from app.db.session import get_db
from app.events.models import Event, EventImage
from app.events.schemas import Category
from app.friends.models import Friendship
from app.notifications.models import Notification
from app.reviews.models import Review
from app.tickets.models import Tickets
from app.users.models import User
from app.users.schemas import Role


@contextmanager
def get_db_session():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def seed_database():
    with get_db_session() as db:
        fake = Faker()

        inspector = inspect(db.get_bind())
        if 'users' in inspector.get_table_names():
            if db.query(User).count() > 0:
                print("Database is not empty - skipping seeding")
                return

        users = []
        for _ in range(20):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                username=fake.unique.user_name(),
                password=fake.password(),
                balance=round(random.uniform(0, 1000), 2),
                role=random.choice(list(Role)),
                password_reset_question=fake.sentence()
            )
            db.add(user)
            users.append(user)
        db.commit()


        for _ in range(30):
            user1, user2 = random.sample(users, 2)
            if not db.query(Friendship).filter(
                    (Friendship.user_id == user1.id) & (Friendship.friend_id == user2.id)
            ).first():
                friendship = Friendship(
                user_id=user1.id,
                friend_id=user2.id
            )
            db.add(friendship)
    db.commit()


    events = []
    categories = list(Category)
    for _ in range(15):
        creator = random.choice(users)
        event = Event(
            name=fake.unique.catch_phrase(),
            description=fake.text(),
            price=round(random.uniform(10, 500), 2),
            data=datetime.now() + timedelta(days=random.randint(1, 365)),
            venue=fake.address(),
            category=random.choice(categories),
            creator=creator.id,
            total_tickets=random.randint(10, 100)
        )
        db.add(event)
        events.append(event)
    db.commit()


    # for event in events:
    #     for _ in range(random.randint(1, 3)):
    #         image = EventImage(
    #             event_id=event.id,
    #             image_url=f"https://picsum.photos/seed/{fake.word()}/800/600"
    #         )
    #         db.add(image)
    # db.commit()

    # Створюємо квитки
    for event in events:
        ticket_users = random.sample(users, random.randint(1, min(10, len(users))))
        for user in ticket_users:
            if not db.query(Tickets).filter(
                    (Tickets.event_id == event.id) & (Tickets.user_id == user.id)
            ).first():
                ticket = Tickets(
                    event_id=event.id,
                    user_id=user.id
                )
                db.add(ticket)
    db.commit()


    for event in events:
        reviewers = random.sample(users, random.randint(1, min(5, len(users))))
        for user in reviewers:
            if not db.query(Review).filter(
                    (Review.event_id == event.id) & (Review.user_id == user.id)
            ).first():
                review = Review(
                    rating=random.randint(1, 5),
                    description=fake.paragraph(),
                    event_id=event.id,
                    user_id=user.id
                )
                db.add(review)
    db.commit()


    tickets = db.query(Tickets).all()
    for ticket in random.sample(tickets, min(20, len(tickets))):
        notification = Notification(
            message=fake.sentence(),
            ticket_id=ticket.id,
            is_read=random.choice([True, False])
        )
        db.add(notification)
    db.commit()

    print("Database seeded successfully!")