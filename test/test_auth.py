from .utils import *
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, validate_current_user
from fastapi import status, HTTPException
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'test_password', db)
    assert authenticated_user is not None
    assert  authenticated_user.username == test_user.username


def test_create_access_token(test_user):
    token = create_access_token(test_user.username, test_user.id, test_user.role, timedelta(days=1))

    decoded_token = jwt.decode(token, SECRET_KEY, [ALGORITHM], options={'verify_signature': False})

    username = decoded_token.get("sub")
    user_id = decoded_token.get("id")
    role = decoded_token.get("role")

    assert username == test_user.username
    assert user_id == test_user.id
    assert role == test_user.role


@pytest.mark.asyncio
async def test_validate_current_user():
    payload = {
        'sub': 'Swanky',
        'id': 1,
        'role': 'admin'
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    user = await validate_current_user(token)
    assert user == {'username': "Swanky", 'user_id': 1, 'role': "admin"}


@pytest.mark.asyncio
async def test_validate_current_user_invalid():
    payload = {
        'role': 'user'
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await validate_current_user(token=token)


    assert excinfo.value.status_code == 401
