from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


import crud
import models
import schemas
from database import SessionLocal, engine

# Create database tables when the backend starts.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple FastAPI React ToDo")


@app.on_event("startup")
def seed_default_user():
    """Create user id=1 so the existing frontend can create tasks.

    The original app hardcodes user id 1. This startup function makes sure that
    user exists automatically, so you do not need to create it manually in /docs.
    """

    db = SessionLocal()
    try:
        if not crud.get_user(db, 1):
            crud.create_user(
                db,
                schemas.UserCreate(email="default@todo.app", password="password"),
            )
    finally:
        db.close()


# Allow the React development server and Docker/Nginx frontend to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """Give each request its own database session and close it afterwards."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    """Friendly message for http://localhost:4000."""

    return {"message": "Backend is running. Open /docs for the API docs."}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    """Return all users."""

    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Return one user by id."""

    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    """Create a ToDo item for a user."""

    if crud.get_user(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_item(db, user_id, item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    """Return all ToDo items."""

    return crud.get_items(db)


@app.put("/items/{item_id}/", response_model=schemas.Item)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    """Update a ToDo item."""

    return crud.update_item(db, item_id, item)


@app.delete("/items/{item_id}/")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a ToDo item."""

    return crud.delete_item(db, item_id)

@app.get("/keyvault-test")
def keyvault_test():
    vault_url = "https://taskapp-kv247.vault.azure.net/"

    credential = DefaultAzureCredential()

    client = SecretClient(
        vault_url=vault_url,
        credential=credential
    )

    secret = client.get_secret("test-secret")

    return {
        "keyvault": "connected",
        "secret_name": secret.name,
        "secret_loaded": bool(secret.value)
    }
