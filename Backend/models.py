from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """Database table for app users.

    The original app uses a hardcoded user with id=1, so this project keeps
    users simple and focuses on the ToDo list behavior.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # One user can own many ToDo items.
    items = relationship("Item", back_populates="owner")


class Item(Base):
    """Database table for ToDo items."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Each item belongs to one user.
    owner = relationship("User", back_populates="items")
