from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """Database table for app users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # SQL Server requires a defined length for indexed string columns.
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Bcrypt hashes are normally ~60 characters.
    # 255 gives us plenty of room.
    hashed_password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    """Database table for ToDo items."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    # Defined length so SQL Server can index this column.
    content = Column(String(500), index=True, nullable=False)

    is_active = Column(Boolean, default=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")