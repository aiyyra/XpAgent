"""This file contains the Message model for the application."""

from datetime import (
    UTC,
    datetime,
    timedelta,
)

from sqlmodel import (
    Field,
    SQLModel,
)

# consider using enums to handle types, but we use string for now.

class Message(SQLModel, table=True):
    """Thread model for storing conversation threads.

    Attributes:
        id: The primary key of the chat
        thread_id: foreign key to thread table
        content-type: text or image or etc (do text and image for now)
        content: actual messages or image url
        message-type:  (Human or AI) can even be tool message
        created_at: When the thread was created
        expires_at: When the thread expires
    """
    # may add payload with jsond to handle tool message 

    id: str = Field(primary_key=True)
    thread_id: str = Field(foreign_key="thread.id")
    message_type: str = Field()
    content_type: str = Field()
    content: str = Field()
    # payload: str = Field(default="")

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(UTC) + timedelta(days=7))
