from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


# This file contains small database helper functions.
# main.py handles HTTP routes; crud.py handles database reads/writes.


def get_user(db: Session, user_id: int):
    """Return one user by id, or None if it does not exist."""

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Return one user by email, or None if it does not exist."""

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    """Return all users."""

    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Create a user with a bcrypt-hashed password."""

    from auth import hash_password

    db_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, user_id: int):
    """Return ToDo items owned by one user."""

    return db.query(models.Item).filter(models.Item.owner_id == user_id).order_by(models.Item.id).all()


def create_item(db: Session, user_id: int, item: schemas.ItemCreate):
    """Create a ToDo item for a user."""

    db_item = models.Item(
        content=item.content,
        is_active=item.is_active,
        owner_id=user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemCreate, user_id: int):
    """Update a ToDo item's text and active/completed state."""

    db_item = db.get(models.Item, item_id)
    if db_item is None or db_item.owner_id != user_id:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.content = item.content
    db_item.is_active = item.is_active
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, user_id: int):
    """Delete a ToDo item."""

    db_item = db.get(models.Item, item_id)
    if db_item is None or db_item.owner_id != user_id:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": f"Task {item_id} was deleted"}
