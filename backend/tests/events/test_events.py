from datetime import datetime, timedelta
from io import BytesIO
from unittest import mock

from fastapi import UploadFile

from app.events.schemas import Category
from  ..utils import test_user, test_events, test_events_images





def test_get_events_data(client, test_events):
    response = client.get("/events?page=1&per_page=10", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == test_events.name
    assert data["description"] == test_events.description
    assert data["price"] == test_events.price
    # assert data["data"] == test_events.data
    assert data["venue"] == test_events.venue
    # assert data["category"] == test_events.category
    assert data["total_tickets"] == test_events.total_tickets
    assert data["images"] == test_events.images





def test_get_my_events_data(client, test_events):
    response = client.get("/events/my", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data[0]["description"] == "This is a test event"
    assert data[0]["price"] == 100.0
    assert data[0]["total_tickets"] == 100

def test_get_some_user_events_data(admin, test_events, test_user):
    response = admin.get(
        f"/events/admin/user/{test_user.id}",
        headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data[0]["description"] == "This is a test event"
    assert data[0]["price"] == 100.0
    assert data[0]["total_tickets"] == 100




@mock.patch("app.events.routes.save_file")
def test_create_events_data(mock_save_file, client, test_user):
    mock_file = "/path/to/new/image.jpg"
    mock_save_file.return_value = mock_file
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(fake_file_content),
    )
    event_data = {

        "name": "Test Event",
        "description": "This is a test event",
        "price": 100.0,
        "data": (datetime.now() + timedelta(days=1)).isoformat(),
        "venue": "Test Venue",
        "category": Category.other.value,
        "creator": test_user.id,
        "total_tickets": 100,

    }



    response = client.post(
        "/events/create-event",
        headers={"Authorization": "Bearer valid_token"},
        params=event_data,
        files=[
            ("images", ("test_image_1.jpeg", fake_file.file, "image/jpeg")),
            ("images", ("test_image_2.jpeg", fake_file.file, "image/jpeg")),
        ]

    )
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == event_data["name"]
    assert data["description"] == event_data["description"]
    assert data["price"] == event_data["price"]
    assert data["data"] == event_data["data"].format()  # Перевіряємо, що дата у форматі ISO 8601
    assert data["venue"] == event_data["venue"]
    assert data["category"] == event_data["category"]
    assert data["total_tickets"] == event_data["total_tickets"]
    assert data["images"][0]["image_url"] == mock_file



@mock.patch("app.events.routes.save_file")
def test_admin_create_events_data(mock_save_file, admin, test_user):
    mock_file = "/path/to/new/image.jpg"
    mock_save_file.return_value = mock_file
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(fake_file_content),
    )
    event_data = {
        "name": "Test Event",
        "description": "This is a test event",
        "price": 100.0,
        "data": (datetime.now() + timedelta(days=1)).isoformat(),
        "venue": "Test Venue",
        "category": Category.other.value,
        "creator": test_user.id,
        "total_tickets": 100,
    }

    response = admin.post(
        f"/events/admin/user/{test_user.id}/create-event",
        headers={"Authorization": "Bearer valid_token"},
        params=event_data,
        files=[
            ("images", ("test_image_1.jpeg", fake_file.file, "image/jpeg")),
            ("images", ("test_image_2.jpeg", fake_file.file, "image/jpeg")),
        ]
    )
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == event_data["name"]
    assert data["description"] == event_data["description"]
    assert data["price"] == event_data["price"]
    assert data["data"] == event_data["data"].format()  # Check ISO 8601 date format
    assert data["venue"] == event_data["venue"]
    assert data["category"] == event_data["category"]
    assert data["total_tickets"] == event_data["total_tickets"]
    assert data["images"][0]["image_url"] == mock_file



def test_delete_events_data(client, test_db, test_events):
    response = client.delete(f"/events/{test_events.id}/delete", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 204

    response = client.get(f"/events/{test_events.id}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 404


@mock.patch("app.events.routes.save_file")
def test_edit_events(mock_save_file, client, test_db, test_events):
    mock_file = "/path/to/new/image.jpg"
    mock_save_file.return_value = mock_file
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(fake_file_content),
    )

    event_data = {
        "event_id": test_events.id,
        "name": "Test  Change Event",
        "description": "This is a test edit event",
        "category": Category.other.value,
        "price": 150.0,
        "data": (datetime.now() + timedelta(days=6)).isoformat(),
        "venue": "Test NEW Venue",
        "total_tickets": 150,

    }

    response = client.put(
        f"/events/{test_events.id}/edit",
        headers={"Authorization": "Bearer valid_token"},
        params=event_data,
        files = [
            ("images", ("test_image_1.jpeg", fake_file.file, "image/jpeg")),
            ("images", ("test_image_2.jpeg", fake_file.file, "image/jpeg")),
    ]

    # files = [
        #     ("name", (None, "Jane Updated")),
        #     ("description", (None, "Doe Updated")),
        #     ("venue", (None, "janedoe_updated@example.com")),
        #     ("category", (None, Category.other)),
        #     ("price", (None, 100.0)),
        #     ("total_tickets", (None, 50)),
        #     # ("data", ("test_image.png", fake_file.file, "image/png")),  # Файл
        # ],
    )
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == event_data["name"]
    assert data["description"] == event_data["description"]
    assert data["price"] == event_data["price"]
    assert data["data"] == event_data["data"].format()  # Перевіряємо, що дата у форматі ISO 8601
    assert data["venue"] == event_data["venue"]
    assert data["category"] == event_data["category"]
    assert data["total_tickets"] == event_data["total_tickets"]


@mock.patch("app.events.crud.delete_file")
def test_delete_image_data(mock_delete_file , client, test_db, test_events_images):
    mock_delete_file.return_value = None
    response = client.delete(f"/events/{test_events_images.id}/images/{1}", headers={"Authorization": "Bearer valid_token"})
    print(response, "*" *  100)
    assert response.status_code == 204


def test_get_event_data(client, test_events, test_user):
    response = client.get(f"/events/{test_events.id}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Event"
    assert data["description"] == "This is a test event"
    assert data["price"] == 100.0
    assert data["venue"] == "Test Venue"
    assert data["category"] == Category.other.value
    assert data["total_tickets"] == 100




def test_filter_events(client, test_events):
    # response = client.get("events/filter", params={"start_date": "2023-10-01", "end_date": "2023-10-02"})
    # assert response.status_code == 200
    # assert len(response.json()) == 2


    response = client.get("events/filter", params={"min_price": 50.0, "max_price": 200.0})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()["items"][0]["name"] == "Test Event"


    response = client.get("events/filter", params={"category": Category.other.value})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()["items"][0]["name"] == "Test Event"

    response = client.get("events/filter", params={"search_term": "Test Event"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()["items"][0]["name"] == "Test Event"

    response = client.get("events/filter", params={"page": 1, "per_page": 10, "totalCount": True})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()["totalCount"] > 0









