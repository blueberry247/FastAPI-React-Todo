from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import auth
import blob_routes
import crud
import models
import schemas
from database import DATABASE_URL, SessionLocal, engine


app = FastAPI(
    title="Simple FastAPI React ToDo",
    servers=[{"url": "https://api.mfarooq.it.com"}],
)
app.include_router(blob_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "https://www.mfarooq.it.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def prepare_database():
    if not DATABASE_URL.startswith("sqlite"):
        return

    try:
        models.Base.metadata.create_all(bind=engine)
        seed_default_user()
    except SQLAlchemyError as exc:
        print(f"Database startup skipped: {exc.__class__.__name__}")


def seed_default_user():
    db = SessionLocal()
    try:
        default_user = crud.get_user_by_email(db, "default@todo.app")

        if not default_user:
            crud.create_user(db, schemas.UserCreate(email="default@todo.app", password="password"))
            return

        changed = False
        if default_user.hashed_password == "password-demo-hash":
            default_user.hashed_password = auth.hash_password("password")
            changed = True

        if default_user.is_active is not True:
            default_user.is_active = True
            changed = True

        if changed:
            db.commit()
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"message": "Backend is running. Open /docs for the API docs."}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token = auth.create_access_token(subject=user.email)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="JWT signing key is unavailable",
        ) from exc

    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@app.post("/items/", response_model=schemas.Item)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.create_item(db, current_user.id, item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.get_items(db, current_user.id)


@app.put("/items/{item_id}/", response_model=schemas.Item)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.update_item(db, item_id, item, current_user.id)


@app.delete("/items/{item_id}/")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return crud.delete_item(db, item_id, current_user.id)
