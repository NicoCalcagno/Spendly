from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class User(UserBase):
    """Public user schema (without sensitive fields)"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
