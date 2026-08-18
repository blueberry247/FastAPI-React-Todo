from datetime import datetime, timedelta, timezone

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import crud
import models

from database import SessionLocal
from keyvault import get_jwt_secret_key


# =========================================================
# JWT CONFIGURATION
# =========================================================

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# PASSWORD HASHING
# =========================================================

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# BEARER TOKEN
# =========================================================

bearer_scheme = HTTPBearer()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================================================
# PASSWORD FUNCTIONS
# =========================================================


def hash_password(
    password: str
) -> str:
    """
    Convert plaintext password into bcrypt hash.
    """

    return password_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Compare plaintext password against stored bcrypt hash.
    """

    if not hashed_password:
        return False

    if password_context.identify(
        hashed_password
    ):
        return password_context.verify(
            plain_password,
            hashed_password
        )

    return False


# =========================================================
# USER AUTHENTICATION
# =========================================================


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    """
    Authenticate a user using email and password.

    Supports migrating the original demo password format.
    """

    user = crud.get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    # -----------------------------------------------------
    # Normal bcrypt password verification
    # -----------------------------------------------------

    if verify_password(
        password,
        user.hashed_password
    ):

        # Inactive users cannot log in
        if not user.is_active:
            return None

        return user

    # -----------------------------------------------------
    # Legacy demo password migration
    # -----------------------------------------------------

    legacy_hash = (
        f"{password}-demo-hash"
    )

    if user.hashed_password == legacy_hash:

        if not user.is_active:
            return None

        user.hashed_password = hash_password(
            password
        )

        db.commit()

        db.refresh(user)

        return user

    return None


# =========================================================
# CREATE JWT TOKEN
# =========================================================


def create_access_token(
    subject: str,
    user_id: int | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT token.

    Signing key is retrieved from Azure Key Vault.
    """

    expire = (
        datetime.now(timezone.utc)
        + (
            expires_delta
            or timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    if user_id is not None:
        payload["user_id"] = user_id

    secret_key = get_jwt_secret_key()

    return jwt.encode(
        payload,
        secret_key,
        algorithm=ALGORITHM,
    )


# =========================================================
# DECODE JWT TOKEN
# =========================================================


def decode_access_token(
    token: str
) -> dict:
    """
    Validate and decode JWT token.
    """

    try:

        secret_key = get_jwt_secret_key()

        return jwt.decode(
            token,
            secret_key,
            algorithms=[ALGORITHM],
        )

    except InvalidTokenError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc


def get_current_token_claims(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return payload


# =========================================================
# CURRENT AUTHENTICATED USER
# =========================================================


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(
        get_db
    ),
) -> models.User:
    """
    Validate bearer token and return authenticated user.
    """

    payload = decode_access_token(credentials.credentials)

    email = payload.get(
        "sub"
    )

    if not email:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    user = crud.get_user_by_email(
        db,
        email
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    if user.is_active is not True:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user
