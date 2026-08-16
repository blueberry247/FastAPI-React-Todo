from typing import List

from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    """Data the frontend sends when creating or updating a ToDo item."""

    content: str
    is_active: bool = True


class Item(ItemCreate):
    """Data the backend returns for a ToDo item."""

    id: int
    owner_id: int

    # Allows Pydantic to read SQLAlchemy model objects directly.
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Data required to create a user."""

    email: str
    password: str


class User(BaseModel):
    """Data the backend returns for a user."""

    id: int
    email: str
    is_active: bool
    items: List[Item] = []

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Credentials submitted by the login page."""

    email: str
    password: str


class Token(BaseModel):
    """JWT response returned after successful login."""

    access_token: str
    token_type: str
