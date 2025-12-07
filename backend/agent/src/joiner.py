from typing import Dict, List, Sequence, Union
from langgraph.graph import MessagesState
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig


class FinalResponse(BaseModel):
    """The final response/answer."""

    response: Union[str, Dict]

class Replan(BaseModel):
    feedback: str = Field(
        description="Analysis of the previous attempts and recommendations on what needs to be fixed."
    )

class JoinOutput(BaseModel):
    """Decide whether to replan or whether you can return the final response."""

    thought: str = Field(
        description="The chain of thought reasoning for the selected action"
    )
    action: Union[FinalResponse, Replan]

def parse_joiner_output(decision: JoinOutput):
    response = [AIMessage(content=f"Thought: {decision.thought}")]
    if isinstance(decision.action, Replan):
        return { "messages": response + [
            SystemMessage(content=f"Content from last attempt: {decision.action.feedback}")
        ]}
    else:
        # return response + [AIMessage(content=f"Final Response: {decision.action.response}")] 
        return { "messages": response + [AIMessage(content=f"Final Response: {decision.action.response}")] } # type: ignore
    

def select_recent_messages(state: MessagesState) -> dict:
    messages = state["messages"]
    selected = []
    is_new_query = False
    if isinstance(messages[::-1][0], HumanMessage):
        is_new_query = True
    for msg in messages[::-1]: 
        selected.append(msg)
        if isinstance(msg, HumanMessage) and not is_new_query:
            break
    return {"messages": selected[::-1]}