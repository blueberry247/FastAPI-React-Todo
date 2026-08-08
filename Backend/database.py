import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Docker Compose sets DATABASE_URL so the SQLite file is stored in a volume.
# If the variable is missing, local development uses a SQLite file in Backend/.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# SQLite needs this option because FastAPI can use multiple threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# SQLAlchemy engine = connection manager for the database.
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal creates one database session per request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is used by models.py to define database tables.
Base = declarative_base()
