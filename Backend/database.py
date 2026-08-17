import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from keyvault import get_secret_client


# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------

def get_database_url():
    """
    Azure:
        Read the ODBC connection string from Azure Key Vault.

    Local development:
        Fall back to DATABASE_URL if supplied.
        Otherwise use SQLite.
    """

    # Local override if required
    local_database_url = os.getenv("DATABASE_URL")

    if local_database_url:
        return local_database_url

    try:
        # Azure App Service uses Managed Identity here.
        secret_client = get_secret_client()

        secret = secret_client.get_secret("database-url")

        odbc_connection_string = secret.value

        encoded_connection_string = quote_plus(
            odbc_connection_string
        )

        return (
            "mssql+pyodbc:///?odbc_connect="
            + encoded_connection_string
        )

    except Exception:
        # Local development fallback
        return "sqlite:///./sql_app.db"


DATABASE_URL = get_database_url()


# ---------------------------------------------------------
# SQLAlchemy engine
# ---------------------------------------------------------

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }
else:
    connect_args = {}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)


# ---------------------------------------------------------
# Database sessions
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------
# SQLAlchemy Base
# ---------------------------------------------------------

Base = declarative_base()