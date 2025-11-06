from pydantic import BaseModel, Field, field_validator


class ThreadResponse(BaseModel):
    """Response model for session creation.

    Attributes:
        thread_id: The unique identifier for the chat session
        name: Name of the thread (defaults to empty string)
    """

    session_id: str = Field(..., description="The unique identifier for the chat session")
    name: str = Field(default="", description="Name of the session", max_length=100)

    # @field_validator("name")
    # @classmethod
    # def sanitize_name(cls, v: str) -> str:
    #     """Sanitize the session name.

    #     Args:
    #         v: The name to sanitize

    #     Returns:
    #         str: The sanitized name
    #     """
    #     # Remove any potentially harmful characters
    #     sanitized = re.sub(r'[<>{}[\]()\'"`]', "", v)
    #     return sanitized

class MessageRequest(BaseModel):
    """Message request model."""
    query: str = Field(..., description="The query to send to the chatbot")