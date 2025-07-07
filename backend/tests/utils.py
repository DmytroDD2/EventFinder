from datetime import datetime, timedelta
from unicodedata import category

import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.events.models import Event, EventImage
from app.events.schemas import Category
from app.friends.models import Friendship
from app.notifications.models import Notification
from app.reviews.models import Review
from app.tickets.models import Tickets
from app.users.models import User
# from tests.conftest import TEST_DATABASE_URL



@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_user(test_db):
    user = User(
        id=1,
        username="janedoe",
        role="user",
        first_name="Jane",
        last_name="Doe",
        balance=200,
        email="janedoe@example.com",
        password="securepassword",
        password_reset_question="secret_question"

    )
    test_db.add(user)
    test_db.commit()

    yield user

    test_db.delete(user)
    test_db.commit()

@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_admin(test_db):
    user = User(
        id=2,
        username="admin",
        role="admin",
        first_name="Jane",
        last_name="Doe",
        email="admin@example.com",
        password="securepassword",
        password_reset_question="secret_question"
    )
    test_db.add(user)
    test_db.commit()

    yield user

    test_db.delete(user)
    test_db.commit()



@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_events(test_db, test_user):
    event = Event(
        id = 1,
        name="Test Event",
        description="This is a test event",
        price=100.0,
        data=datetime.now() + timedelta(days=1),
        venue="Test Venue",
        category=Category.other,
        creator=test_user.id,
        total_tickets=100
    )
    test_db.add(event)
    test_db.commit()

    yield event

    test_db.delete(event)
    test_db.commit()




@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_events_images(test_db, test_user):
    event = Event(
        id = 2,
        name="Test Event",
        description="This is a test event",
        price=100.0,
        data=datetime.now() + timedelta(days=1),
        venue="Test Venue",
        category=Category.other,
        creator=test_user.id,
        total_tickets=100
    )
    images = ["1", "2", "3"]
    db_images = [EventImage(event_id=1, image_url=image, id=number) for number, image in enumerate(images)]
    event.images = db_images
    test_db.add(event)
    test_db.commit()

    yield event

    test_db.delete(event)
    test_db.commit()



@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_events_reviews(test_db):
    user = User(
        id=4,
        username="j",
        role="user",
        first_name="Jane",
        last_name="Doe",
        email="j@example.com",
        password="securepassword",
        password_reset_question="secret_question"
    )
    test_db.add(user)
    test_db.commit()


    events = ["first", "second", "third"]
    db_events = [Event(name=event, id=number + 1, category=Category.other, creator=user.id) for number, event in enumerate(events)]
    test_db.add_all(db_events)
    test_db.commit()


    review_ls = [(5, "good event"), (6, "not well"), (3, "can`t complain")]
    db_review = [
        Review(event_id=event.id, user_id=user.id, rating=review[0], description=review[1], id=number + 1)
        for number, (event, review) in enumerate(zip(db_events, review_ls))
    ]
    test_db.add_all(db_review)
    test_db.commit()

    yield db_review


    test_db.delete(user)
    test_db.commit()



@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_user_reviews(test_db, test_user):
    user = User(
        id=4,
        username="j",
        role="user",
        first_name="Jane",
        last_name="Doe",
        email="j@example.com",
        password="securepassword",
        password_reset_question="secret_question"
    )
    test_db.add(user)
    test_db.commit()


    events = ["first", "second", "third"]
    db_events = [Event(name=event, id=number + 1, category=Category.other, creator=user.id) for number, event in enumerate(events)]
    test_db.add_all(db_events)
    test_db.commit()


    review_ls = [(5, "good event"), (6, "not well"), (3, "can`t complain")]
    db_review = [
        Review(event_id=event.id, user_id=test_user.id, rating=review[0], description=review[1], id=number + 1)
        for number, (event, review) in enumerate(zip(db_events, review_ls))
    ]
    test_db.add_all(db_review)
    test_db.commit()

    yield db_review


    test_db.delete(user)
    test_db.commit()

@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_user_tickets(test_db, test_user):
    # Створюємо користувача
    user = User(
        id=4,
        username="j",
        role="user",
        first_name="Jane",
        last_name="Doe",
        email="j@example.com",
        password="securepassword",
        password_reset_question="secret_question"
    )
    test_db.add(user)
    test_db.commit()

    events = [
        "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
        "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth"
    ]

    db_events = [Event(name=event, id=number + 1, category=Category.other, creator=user.id) for number, event in enumerate(events)]

    test_db.add_all(db_events)
    test_db.commit()



    db_tickets = [
        Tickets(event_id=number, user_id=test_user.id, id=number)
        for number  in range(1, len(events) + 1)
    ]
    test_db.add_all(db_tickets)
    test_db.commit()

    yield db_tickets


    test_db.delete(user)
    test_db.commit()


@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_friend(test_db, test_user):
    friend = User(
        id=6,
        username="Friend",
        role="user",
        first_name="Jane",
        last_name="Doe",
        email="friend@example.com",
        password="securepassword",
        password_reset_question="secret_question",
        profile_picture="/path/to/new/image.jpg"
    )
    test_db.add(friend)
    test_db.commit()

    friends = Friendship(user_id=test_user.id, friend_id=friend.id)
    test_db.add(friends)
    test_db.commit()

    yield friend

    test_db.delete(friend)
    test_db.commit()





@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_user_friend_tickets(test_db, test_friend, test_user):
    # Створюємо користувача
    user = User(
        id=4,
        username="j",
        role="user",
        first_name="Jane",
        last_name="Doe",
        email="j@example.com",
        password="securepassword",
        password_reset_question="secret_question"
    )
    test_db.add(user)
    test_db.commit()


    events = ["first", "second", "third"]
    db_events = [Event(name=event, id=number + 1, category=Category.other, creator=user.id) for number, event in enumerate(events)]
    test_db.add_all(db_events)
    test_db.commit()



    db_tickets = [
        Tickets(event_id=number, user_id=test_friend.id, id=number)
        for number  in range(1, len(db_events) + 1)
    ]
    test_db.add_all(db_tickets)
    test_db.commit()

    yield db_tickets


    test_db.delete(user)
    test_db.commit()

@pytest_asyncio.fixture(scope="function", loop_scope="function")
def test_user_notifications(test_db, test_user_tickets):
    for index, ticket in enumerate(test_user_tickets):
        event = test_db.query(Event).filter_by(id=ticket.event_id).first()
        if event and event.data:
            event_date = event.data.date()
            event_time = event.data.time()
        else:
            event_date = "not yet known"
            event_time = "not yet known"

        message = (
            f'You are registered for the event: {event.name}. '
            f'Start date {event_date} at {event_time}. '
            f'Location: {event.venue}'
        )

        db_notification = Notification(
            id=ticket.id,
            ticket_id=ticket.id,
            message=message,
            is_read=(index % 2 == 1)  # Кожен другий запис має is_read=False
        )
        test_db.add(db_notification)

    test_db.commit()

    yield test_user_tickets

    test_db.query(Notification).delete()
    test_db.commit()


































class TestDatabase:
    def __init__(self, session: Session):
        self.session = session

    def populate_test_database(self):
        user = User(
            id=1,
            username="janedoe",
            role="user",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            password="securepassword",
            password_reset_question="secret_question"
        )
        # product_1 = Product(
        #     name="Product 2",
        #     quantity=10
        # )
        #
        # product_2 = Product(
        #     name="Product 1",
        #     quantity=4
        # )
        #
        # product_3 = Product(
        #     name="Product 3",
        #     quantity=84
        # )
        #
        #self.session.add_all([product_1, product_2, product_3])
        self.session.add_all([user])

        self.session.commit()


# def override_get_db():
#     test_engine = create_engine(TEST_DATABASE_URL)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()