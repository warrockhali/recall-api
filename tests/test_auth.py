from collections.abc import Iterator
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from recall_api.db.models import User
from recall_api.db.session import get_engine, get_session
from recall_api.main import app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[tuple[TestClient, Session]]:
    monkeypatch.setenv("AUTH_SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
    with get_engine().connect() as connection:
        transaction = connection.begin()

        def test_session() -> Iterator[Session]:
            with Session(
                connection, join_transaction_mode="create_savepoint"
            ) as session:
                yield session

        app.dependency_overrides[get_session] = test_session
        try:
            with (
                TestClient(app) as test_client,
                Session(
                    connection, join_transaction_mode="create_savepoint"
                ) as session,
            ):
                yield test_client, session
        finally:
            app.dependency_overrides.clear()
            transaction.rollback()


def test_register_login_and_me(client: tuple[TestClient, Session]) -> None:
    http, session = client
    response = http.post(
        "/auth/register",
        json={"email": "  Person@Example.com  ", "password": "safe-password-123"},
    )
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == "person@example.com"
    assert user["timezone"] == "UTC"
    assert "password_hash" not in user

    stored = session.scalar(select(User).where(User.email == "person@example.com"))
    assert stored is not None
    assert stored.password_hash != "safe-password-123"
    assert stored.password_hash.startswith("$argon2")

    login = http.post(
        "/auth/login",
        json={"email": "PERSON@example.com", "password": "safe-password-123"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    me = http.get(
        "/auth/me", headers={"Authorization": f"Bearer {login.json()['access_token']}"}
    )
    assert me.status_code == 200
    assert me.json()["id"] == user["id"]

    other = http.post(
        "/auth/register",
        json={"email": "other@example.com", "password": "other-password-123"},
    )
    assert other.status_code == 201
    assert other.json()["id"] != user["id"]
    assert (
        http.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {login.json()['access_token']}"},
        ).json()["id"]
        == user["id"]
    )


def test_duplicate_and_invalid_credentials(client: tuple[TestClient, Session]) -> None:
    http, _ = client
    first = {"email": "person@example.com", "password": "safe-password-123"}
    assert http.post("/auth/register", json=first).status_code == 201
    assert (
        http.post(
            "/auth/register", json={**first, "email": "PERSON@example.com"}
        ).status_code
        == 409
    )
    assert (
        http.post("/auth/login", json={**first, "password": "wrong"}).status_code == 401
    )
    assert (
        http.post(
            "/auth/login", json={**first, "email": "unknown@example.com"}
        ).status_code
        == 401
    )
    assert http.post("/auth/login", json=first).status_code == 200


def test_invalid_input_and_token(client: tuple[TestClient, Session]) -> None:
    http, _ = client
    assert (
        http.post(
            "/auth/register", json={"email": "bad", "password": "short"}
        ).status_code
        == 422
    )
    assert http.get("/auth/me").status_code == 401
    assert (
        http.get("/auth/me", headers={"Authorization": "Bearer corrupted"}).status_code
        == 401
    )

    expired = jwt.encode(
        {"sub": "1", "exp": datetime.now(UTC) - timedelta(seconds=1)},
        "test-secret-key-with-at-least-32-bytes",
        algorithm="HS256",
    )
    assert (
        http.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code
        == 401
    )

    missing_exp = jwt.encode(
        {"sub": "1"}, "test-secret-key-with-at-least-32-bytes", algorithm="HS256"
    )
    assert (
        http.get(
            "/auth/me", headers={"Authorization": f"Bearer {missing_exp}"}
        ).status_code
        == 401
    )
