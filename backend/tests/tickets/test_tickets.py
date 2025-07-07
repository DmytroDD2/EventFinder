
from ..utils import test_user_tickets, test_user, test_friend, test_user_friend_tickets, test_events, test_user_tickets



def test_get_all_user_ticket(client, test_user_tickets):
    response = client.get(
        f"/tickets",
        headers={"Authorization": "Bearer valid_token"},


    )
    assert response.status_code == 200
    data = response.json()


    assert isinstance(data, list)

    assert len(data) > 0
    # print(data)
    assert data[0]["event_name"] == "first"
    assert not data[0]["description"]
    assert data[0]["event_id"] == 1
    assert data[0]["creator"] == "janedoe"


def test_get_some_user_tickets(admin, test_user_tickets, test_user):
    response = admin.get(
        f"/tickets/admin/{test_user.id}",
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["event_name"] == "first"
    assert not data[0]["description"]
    assert data[0]["event_id"] == 1
    assert data[0]["creator"] == "janedoe"





def test_get_all_fiend_ticket(client, test_user_friend_tickets):
    response = client.get(
        f"/tickets/friends",
        headers={"Authorization": "Bearer valid_token"},


    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    assert len(data) > 0

    assert data[0]["event_name"] == "first"
    assert not data[0]["description"]
    assert data[0]["event_id"] == 1
    assert data[0]["creator"] == "j"
    assert data[0]["friend_name"] == "Friend"



def test_reserve_ticket(client, test_events, test_user):
    response = client.post(
        f"/tickets/{test_events.id}/reserve",
        headers={"Authorization": "Bearer valid_token"},


    )
    assert response.status_code == 201
    data = response.json()




def test_delete_ticket(client, test_user_tickets):
    response = client.delete(
        f"/tickets/1/delete",
        headers={"Authorization": "Bearer valid_token"},


    )
    assert response.status_code == 204








