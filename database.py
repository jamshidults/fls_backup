# database.py
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_database_path():
    # Get the base path from environment or use a default
    base_path = os.environ.get('HOME', os.path.expanduser('~'))

    # Construct the full path
    db_path = os.path.join(base_path, 'shared_folder', 'LOG_DB', 'current', 'orders.db')

    # Create directory if it doesn't exist
    db_directory = os.path.dirname(db_path)
    os.makedirs(db_directory, exist_ok=True)

    return f"sqlite+aiosqlite:///{db_path}"


# Get the database URL, creating path if necessary
SQLALCHEMY_DATABASE_URL = get_database_path()


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()