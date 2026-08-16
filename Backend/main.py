from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import auth
import crud
import models
import schemas
from database import SessionLocal, engine


# ---------------------------------------------------------
# Create database tables
# ---------------------------------------------------------

models.Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(title="Simple FastAPI React ToDo")


# ---------------------------------------------------------
# Startup - create/migrate default user
# ---------------------------------------------------------

@app.on_event("startup")
def seed_default_user():
    """
    Create or migrate the default user used by the existing ToDo flow.

    This also repairs older database records that may not have
    is_active=True.
    """

    db = SessionLocal()

    try:
        default_user = crud.get_user_by_email(
            db,
            "default@todo.app"
        )

        # -------------------------------------------------
        # Create default user if it does not exist
        # -------------------------------------------------

        if not default_user:
            crud.create_user(
                db,
                schemas.UserCreate(
                    email="default@todo.app",
                    password="password",
                ),
            )

        # -------------------------------------------------
        # Migrate old user if already present
        # -------------------------------------------------

        else:
            changed = False

            # Convert old demo password marker into bcrypt hash
            if default_user.hashed_password == "password-demo-hash":
                default_user.hashed_password = auth.hash_password(
                    "password"
                )
                changed = True

            # Repair users created before is_active existed
            if default_user.is_active is not True:
                default_user.is_active = True
                changed = True

            if changed:
                db.commit()
                db.refresh(default_user)

    finally:
        db.close()


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Database dependency
# ---------------------------------------------------------

def get_db():
    """
    Give each request its own database session and
    close it afterwards.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/")
def health_check():
    """
    Basic backend health endpoint.
    """

    return {
        "message": "Backend is running. Open /docs for the API docs."
    }


# =========================================================
# USERS
# =========================================================


# ---------------------------------------------------------
# Create User
# ---------------------------------------------------------

@app.post(
    "/users/",
    response_model=schemas.User
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    """

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud.create_user(
        db,
        user
    )


# =========================================================
# AUTHENTICATION
# =========================================================


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

@app.post(
    "/login",
    response_model=schemas.Token
)
def login(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    """
    Verify user credentials and return a JWT access token.

    JWT signing key is retrieved from Azure Key Vault.
    """

    user = auth.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    try:
        token = auth.create_access_token(
            subject=user.email
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="JWT signing key is unavailable",
        ) from exc

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# ---------------------------------------------------------
# Current User
# ---------------------------------------------------------

@app.get(
    "/users/me",
    response_model=schemas.User
)
def read_current_user(
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Return currently authenticated user.
    """

    return current_user


# ---------------------------------------------------------
# Read All Users
# ---------------------------------------------------------

@app.get(
    "/users/",
    response_model=List[schemas.User]
)
def read_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Return all users.

    Requires authentication.
    """

    return crud.get_users(db)


# ---------------------------------------------------------
# Read User
# ---------------------------------------------------------

@app.get(
    "/users/{user_id}",
    response_model=schemas.User
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Return one user by ID.

    Requires authentication.
    """

    user = crud.get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================================================
# TODO ITEMS
# =========================================================


# ---------------------------------------------------------
# Create Item For User
# ---------------------------------------------------------

@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item
)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Create a ToDo item.

    A user can only create tasks for themselves.
    """

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot create tasks for another user"
        )

    return crud.create_item(
        db,
        current_user.id,
        item
    )


# ---------------------------------------------------------
# Create Item
# ---------------------------------------------------------

@app.post(
    "/items/",
    response_model=schemas.Item
)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Create a ToDo item for authenticated user.
    """

    return crud.create_item(
        db,
        current_user.id,
        item
    )


# ---------------------------------------------------------
# Read Items
# ---------------------------------------------------------

@app.get(
    "/items/",
    response_model=List[schemas.Item]
)
def read_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Return authenticated user's ToDo items.
    """

    return crud.get_items(
        db,
        current_user.id
    )


# ---------------------------------------------------------
# Update Item
# ---------------------------------------------------------

@app.put(
    "/items/{item_id}/",
    response_model=schemas.Item
)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Update a ToDo item.

    Ownership is enforced.
    """

    return crud.update_item(
        db,
        item_id,
        item,
        current_user.id
    )


# ---------------------------------------------------------
# Delete Item
# ---------------------------------------------------------

@app.delete(
    "/items/{item_id}/"
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),
):
    """
    Delete a ToDo item.

    Ownership is enforced.
    """

    return crud.delete_item(
        db,
        item_id,
        current_user.id
    )