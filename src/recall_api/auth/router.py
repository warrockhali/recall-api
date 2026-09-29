from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from recall_api.auth.schemas import LoginInput, RegisterInput, TokenRead, UserRead
from recall_api.auth.service import (
    DuplicateEmailError,
    authenticate,
    create_access_token,
    register,
    user_id_from_token,
)
from recall_api.db.models import User
from recall_api.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    credentials: RegisterInput, session: Annotated[Session, Depends(get_session)]
) -> User:
    try:
        return register(session, str(credentials.email), credentials.password)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Email already registered"
        ) from exc


@router.post("/login", response_model=TokenRead)
def login(
    credentials: LoginInput, session: Annotated[Session, Depends(get_session)]
) -> TokenRead:
    user = authenticate(session, str(credentials.email), credentials.password)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return TokenRead(access_token=create_access_token(user.id))


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    user_id = user_id_from_token(credentials.credentials) if credentials else None
    user = session.get(User, user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/me", response_model=UserRead)
def read_current_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
