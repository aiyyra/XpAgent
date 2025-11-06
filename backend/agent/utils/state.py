from langgraph.graph import MessagesState
from pydantic import BaseModel

class ExtendedMessagesState(MessagesState):
    points: str
# class State:


# Temp State to try the code first. (Not actual state for the project)
class TestState(MessagesState):
    points: int


class State(BaseModel):
    # messages: MessagesState
    # points: int
    messages_state: MessagesState

class InputState(BaseModel):
    messages: MessagesState
