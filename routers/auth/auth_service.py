from passlib.context import CryptContext
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from repositories import auth_repository as repository
from starlette.responses import RedirectResponse

SECRET_KEY = "AkdFRltXkDDzeV4b1BtUYMbpI5dfyyAtC3GBecIVbCSqiwnN2d7kcGhuNNWtZEdE"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(username: str, password: str, db):
    user = repository.get_user_by_name(db, username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    payload = { 'sub': username, 'id': user_id, 'role': role }
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def validate_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or id is invalid.")
        return {'username': username, 'user_id': user_id, 'role': role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid.")


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def hash_password(password) -> str:
    return bcrypt_context.hash(password)

# Define redirect
def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response