from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_validate_current_user


def test_get_current_user(test_user):
    response = client.get("/user/current_user")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['username'] == 'Swanky'


def test_change_password_success(test_user):
    response = client.put("/user/update_password", json={
        "old_password": "test_password",
        "new_password": "kalp_kalbe_karşı",
        "confirm_new_password": "kalp_kalbe_karşı"
    })

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put("/user/update_password", json={
        "old_password": "test_pass",
        "new_password": "kalp_kalbe_karşı",
        "confirm_new_password": "kalp_kalbe_karşı"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect old password'}