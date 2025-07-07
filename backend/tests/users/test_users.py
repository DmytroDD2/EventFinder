from datetime import timedelta
from io import BytesIO
from unittest import mock

import jwt
from fastapi import UploadFile

from app.users.models import User
from app.users.schemas import Role, UserToken
from app.users.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, check_password
from ..utils import test_admin, test_user





@mock.patch("app.users.routes.send_email_task.delay")
def test_register_user(mock_send_email, client):

    user_data = {
        "id": 4,
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "janeddoe@example.com",
        "username": "jandedoe",
        "password": "securepassword",
        "role": "user",
        "password_reset_question": "secret_question"
    }
    response = client.post("/users/register", json=user_data)
    mock_send_email.assert_called_once()

    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == "jandedoe"
    assert "access_token" in data["token"]



@mock.patch("app.users.routes.authenticate_user")
@mock.patch("app.users.routes.create_token")
def test_login(mock_create_token, mock_authenticate_user, client):

    mock_user = User(
        id=1,
        username="janedoe",
        role=Role.user,
        first_name="Jane",
        last_name="Doe",
        email="janedoe@example.com",
        password="securepassword",
        password_reset_question="secret_question"
        )
    mock_authenticate_user.return_value = mock_user


    mock_create_token.return_value = "fake_token"

    form_data = {
        "username": "janedoe",
        "password": "securepassword"
    }

    response = client.post("/users/token", json=form_data)

    mock_authenticate_user.assert_called_once_with(mock.ANY, "janedoe", "securepassword")
    mock_create_token.assert_any_call(
        {"id": mock_user.id, "role": "user"}, timedelta(minutes=1200)
    )
    mock_create_token.assert_any_call(
        {"id": mock_user.id, "role": "user"}, timedelta(days=7)
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"




@mock.patch("app.users.routes.create_token")
def test_refresh_access_token_success(mock_create_token, client):

    refresh_token_payload = {"id": 1, "role": "user"}
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)


    mock_create_token.return_value = "fake_access_token"


    response = client.post(
        "/users/token/refresh",
        data={"refresh_token": refresh_token}
    )


    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "fake_access_token"
    assert data["token_type"] == "bearer"


    mock_create_token.assert_called_once_with(
        {"id": 1, "role": "user"}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )



def test_refresh_access_token_invalid_token(client):
    response = client.post(
        "/users/token/refresh",
        data={"refresh_token": "invalid_token"}
    )


    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_refresh_access_token_missing_id_or_role(client):
    refresh_token_payload = {"some_key": "some_value"}
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)


    response = client.post(
        "/users/token/refresh",
        data={"refresh_token": refresh_token}
    )


    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}



def test_get_user_data(client, test_user):
    response = client.get("/users", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "janedoe"
    assert data["email"] == "janedoe@example.com"



def test_get_all_users(admin, test_admin):
    response = admin.get("users/all-users", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_user_by_id(admin, test_admin):
    user_id = 2
    response = admin.get(f"/users/admin/{user_id}", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    print(response, "*" * 100)
    data = response.json()
    assert data["id"] == user_id


@mock.patch("app.users.handlers.save_file")
def test_edit_user_data(mock_save_file, client, test_user):
    mock_save_file.return_value = "/path/to/new/image.jpg"
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.png",
        file=BytesIO(fake_file_content),
    )

    response = client.put(
        "/users/change",
        headers={"Authorization": "Bearer valid_token"},
        files=[
            ("first_name", (None, "Jane Updated")),  # Текстове поле
            ("last_name", (None, "Doe Updated")),  # Текстове поле
            ("email", (None, "janedoe_updated@example.com")),  # Текстове поле
            ("profile_picture", ("test_image.png", fake_file.file, "image/png")),  # Файл
        ],
        # data={
        #     "first_name": "Jane Updated",
        #     "last_name": "Doe Updated",
        #     "email": "janedoe_updated@example.com",
        #
        #
        # },
        # files={"profile_picture": ("test_image.png", fake_file.file, "image/png")},

    )

    assert response.status_code == 200
    data = response.json()

    assert data["first_name"] == "Jane Updated"
    assert data["last_name"] == "Doe Updated"
    assert data["email"] == "janedoe_updated@example.com"
    assert data["profile_picture"] == "/path/to/new/image.jpg"

#
#
#
@mock.patch("app.users.routes.save_file")
def test_edit_user_image(mock_save_file, client, test_user):

    mock_save_file.return_value = "/path/to/new/image.jpg"
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(fake_file_content),
    )

    response = client.patch(
        "/users/image",
        headers={"Authorization": "Bearer valid_token"},
        files={"image": ("test_image.jpg", fake_file.file, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["profile_picture"] == "/path/to/new/image.jpg"


    mock_save_file.assert_called_once_with(mock.ANY)


@mock.patch("app.users.routes.save_file")
def test_edit_user_image_by_admin(mock_save_file, admin, test_user):

    mock_save_file.return_value = "/path/to/new/image.jpg"
    fake_file_content = b"fake image content"

    fake_file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(fake_file_content),
    )

    response = admin.patch(
        f"/users/admin/{test_user.id}/image",
        files={"image": ("test_image.jpg", fake_file.file, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["profile_picture"] == "/path/to/new/image.jpg"

    mock_save_file.assert_called_once_with(mock.ANY)


def test_edit_user_password(client, test_user):
    new_password = "new_password"
    response = client.patch(
        "/users/password",
        headers={"Authorization": "Bearer valid_token"},
        json={"password": new_password}
    )

    assert response.status_code == 200

    data = response.json()

    assert check_password(new_password,data["password"])


def test_edit_user_password_by_admin(admin, test_user):
    new_password = "new_password"
    response = admin.patch(
        f"/users/admin/{test_user.id}/password",
        json={"password": new_password}
    )

    assert response.status_code == 200

    data = response.json()

    assert check_password(new_password, data["password"])

def test_request_password_reset(client, test_user):
    new_password = "new_password"
    response = client.patch(
        "/users/password-reset",
        json={
            "username": "janedoe",
            "password_reset_question": "secret_question",
            "new_password": new_password}
    )

    assert response.status_code == 200

    data = response.json()

    assert check_password(new_password,data["password"])







@mock.patch("app.users.routes.send_email_task.delay")
def test_generate_reset_token_on_mail(mock_send_email, client, test_user):
    email = "janedoe@example.com"

    response = client.post(
        "/users/generate-reset-token",
        data={"email": email}
    )

    mock_send_email.assert_called_once()
    assert response.status_code == 200

    data = response.json()
    assert data == f"Reset token sent to {email}"



def test_edit_role(admin, test_db,test_admin, test_user):

    response = admin.patch(
        "/users/role",
        data={"user_id": 1}
    )


    assert response.status_code == 200




def test_recharge_account(client, test_user):
    amount = 100
    response = client.post(
        "/users/recharge",
        json={"amount": amount}
    )


    assert response.status_code == 200
    data =response.json()
    assert data == {"message": f"Account successfully recharged: {float(amount)}. New balance: {test_user.balance}"}

def test_admin_recharge_account(admin, test_user):
    amount = 100
    response = admin.post(
        f"/users/admin/{test_user.id}/recharge",
        json={"amount": amount}
    )


    assert response.status_code == 200
    data = response.json()
    assert data == {"message": f"Account successfully recharged: {float(amount)}. New balance: {test_user.balance}"}





























