from ..utils import test_user_notifications, test_user_tickets, test_user


def test_get_all_notifications(client, test_user_notifications):
    response = client.get("/notifications", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    assert data[0]["is_read"] == False
    assert data[0]["message"] == "You are registered for the event: first. Start date not yet known at not yet known. Location: None"
    assert data[0]["ticket_id"] == 1



def test_get_read_notifications(client, test_user_notifications):
    response = client.get("/notifications/read", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(notification["is_read"] is True for notification in data)


def test_get_unread_notifications(client, test_user_notifications):
    response = client.get("/notifications/unread", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(notification["is_read"] is False for notification in data)



def test_get_notification(client, test_user_notifications):
    response = client.get("/notifications/1", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_read"]
    assert data["message"] == "You are registered for the event: first. Start date not yet known at not yet known. Location: None"
    assert data["ticket_id"] == 1

    second_response = client.get("/notifications/2", headers={"Authorization": "Bearer valid_token"})
    second_data = second_response.json()
    assert second_data["is_read"]
