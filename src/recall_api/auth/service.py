import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from recall_api.db.models import User

_password_hash = PasswordHash.recommended()
_token_algorithm = "HS256"
_token_lifetime = timedelta(minutes=30)


class DuplicateEmailError(Exception):
    pass


def register(session: Session, email: str, password: str) -> User:
    user = User(email=email, password_hash=_password_hash.hash(password))
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        if session.scalar(select(User.id).where(User.email == email)) is not None:
            raise DuplicateEmailError from exc
        raise
    session.refresh(user)
    return user


def authenticate(session: Session, email: str, password: str) -> User | None:
    user = session.scalar(select(User).where(User.email == email))
    if user is None or not _password_hash.verify(password, user.password_hash):
        return None
    return user


def _secret_key() -> str:
    load_dotenv()
    secret = os.getenv("AUTH_SECRET_KEY", "")
    if len(secret.encode()) < 32:
        raise RuntimeError("AUTH_SECRET_KEY must contain at least 32 bytes")
    return secret


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(UTC) + _token_lifetime
    return jwt.encode(
        {"sub": str(user_id), "exp": expires_at},
        _secret_key(),
        algorithm=_token_algorithm,
    )


def user_id_from_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            _secret_key(),
            algorithms=[_token_algorithm],
            options={"require": ["sub", "exp"]},
        )
        user_id = int(payload["sub"])
        return user_id if user_id > 0 else None
    except (InvalidTokenError, ValueError, TypeError):
        return None
