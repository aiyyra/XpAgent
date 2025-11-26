from typing import Optional
from langgraph.graph import MessagesState
from pydantic import BaseModel

class ExtendedMessagesState(MessagesState):
    points: str
# class State:


# Temp State to try the code first. (Not actual state for the project)
class TestState(MessagesState):
    points: int

class TasksPlanning(BaseModel):
    goal: str
    tasks: str
    
class State(MessagesState):
    # messages: MessagesState
    # points: int
    tasks_planning: Optional[TasksPlanning]

class InputState(BaseModel):
    messages: MessagesState

class DBInteractionState(MessagesState):
    query: str