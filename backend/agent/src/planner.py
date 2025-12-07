from typing import Sequence

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableBranch

from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, ToolMessage, FunctionMessage, AIMessage
from langchain_core.prompts import BasePromptTemplate
from langchain.tools import BaseTool

from agent.src.output_parser import M3LXPlanParser

def create_planner(
        llm: ChatOpenAI,
        tools: Sequence[BaseTool],
        base_prompt: BasePromptTemplate,
        database_schema: str = None, # type: ignore
):
    tool_descriptions = "\n".join(
        f"{i}. {tool.description}\n"
        for i, tool in enumerate(tools, start=1)
    )
    planner_prompt = base_prompt.partial(
        replan = "",
        num_tools = str(len(tools) + 1),
        tool_descriptions = tool_descriptions,
    )
    replanner_prompt = base_prompt.partial(
        replan=' - You are given "Previous Plan" which is the plan that the previous agent created along with the execution results '
        "(given as Observation) of each plan and a general thought (given as Thought) about the executed results."
        'You MUST use these information to create the next plan under "Current Plan".\n'
        ' - When starting the Current Plan, you should start with "Thought" that outlines the strategy for the next plan.\n'
        " - In the Current Plan, you should NEVER repeat the actions that are already executed in the Previous Plan.\n"
        " - You must continue the task index from the end of the previous one. Do not repeat task indices.",
        num_tools = str(len(tools) + 1),
        tool_descriptions = tool_descriptions,
    )

    # build a state machine that checks the state or type of the last message
    # if the last message is a system message, we should replan
    def should_replan(messages: list) -> bool:
        if not messages:
            return False
        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            # Case for continuation of chat
            return True
        else : 
            return isinstance(last_message, SystemMessage)
    
    def get_last_index(messages: list):
        next_task = 0
        for message in messages[::-1]: #Can check this implementation again
            if isinstance(message, FunctionMessage):
                next_task = message.additional_kwargs["idx"] + 1
                break
        messages[-1].content = str(messages[-1].content) + f" - Begin counting at : {next_task}"
        return messages
    
    return (
        RunnableBranch(
            (should_replan, get_last_index | replanner_prompt), # branch 1
            planner_prompt, # default branch
        )
        | llm
        | M3LXPlanParser(tools=tools)
    )



