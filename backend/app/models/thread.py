""" This module contains the Thread model. """
from datetime import datetime, timedelta, UTC
from sqlmodel import SQLModel, Field

class Thread(SQLModel, table=True):
    """Thread model for storing conversation threads.

    Attributes:
        id: The primary key of the thread
        topic: The topic of the thread
        created_at: When the thread was created
        expires_at: When the thread expires (good to delete whole thread)
    """
    id: str = Field(primary_key=True)
    topic: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(UTC) + timedelta(days=7))