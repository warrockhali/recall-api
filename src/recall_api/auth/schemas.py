from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailInput(BaseModel):
    email: EmailStr = Field(max_length=320)

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value: str) -> str:
        return value.strip() if isinstance(value, str) else value

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()


class RegisterInput(EmailInput):
    password: str = Field(min_length=8, max_length=128)


class LoginInput(EmailInput):
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    id: int
    email: str
    timezone: str
    created_at: datetime


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
