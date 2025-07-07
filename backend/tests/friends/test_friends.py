from ..utils import test_friend, test_user, test_admin



def test_get_user_friends(client, test_friend):
    response = client.get(
            f"/users/friends",
            headers={"Authorization": "Bearer valid_token"},


        )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["first_name"] == "Jane"
    assert data[0]["last_name"] == "Doe"
    assert data[0]["username"] == "Friend"
    assert data[0]["profile_picture"] == "/path/to/new/image.jpg"
    assert data[0]["id"] == 6


def test_get_some_user_friends(admin, test_friend, test_user):
    response = admin.get(
        f"/users/friends/{test_user.id}",
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data[0]["first_name"] == "Jane"
    assert data[0]["last_name"] == "Doe"
    assert data[0]["username"] == "Friend"
    assert data[0]["profile_picture"] == "/path/to/new/image.jpg"
    assert data[0]["id"] == 6

def test_add_friend(client, test_user, test_admin):
    response = client.post(
            f"/users/friends/{test_admin.id}/add",
            headers={"Authorization": "Bearer valid_token"},
        )
    assert response.status_code == 201


def test_admin_add_friend(admin, test_user, test_admin):
    # Припустимо get_token — фікстура, яка повертає валідний токен для test_admin


    response = admin.post(
        f"/users/friends/admin/{test_admin.id}/{test_user.id}/add",
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 201
    data = response.json()

    # Тут перевіряємо, що в поверненні є інфо про друга (можна адаптувати під структуру)
    assert data["id"] == test_user.id or data.get("friend_id") == test_user.id


def test_remove_friend(client, test_friend):
    response = client.delete(
            f"/users/friends/{test_friend.id}/remove",
            headers={"Authorization": "Bearer valid_token"},


        )
    assert response.status_code == 204

def test_admin_remove_friend(admin, test_friend, test_user):
    response = admin.delete(
        f"/users/friends/admin/{test_user.id}/{test_friend.id}/remove",
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 204

