from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()['username'] == 'testuser'


def test_change_password_success(test_user):
    response = client.put("/users/password", json = {"password": "testpassword",
                                                     "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_passsword(test_user):
    response = client.put("/users/password", json = {"password": "wrongpassword",
                                                     "new_password": "newtestpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    response = client.put("/users/phonenumber/1111111111")
    assert response.status_code == status.HTTP_204_NO_CONTENT