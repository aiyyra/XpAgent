from typing import Literal
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage


from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from pydantic import BaseModel

# from agent.utils.state import TestState  as State
from agent.utils.state import State, TasksPlanning
from agent.utils.test_tools import tools

from langgraph.graph import END

# Define Chat Model
llm = ChatOpenAI(model="gpt-4", temperature=0.0)
llm_with_tools = llm.bind_tools(tools)

# Intent classifier |||||||| we will make intent classifier in later staged when query be more complex
# make class schema for structured output llm to choose its next destination

goal_formation_prompt = """
You are part of an agentic system that has the ability to interact with a SQL database. Make data analysis from it and more.
Given the query, Identify the main and absolute goal of the query. The goal need to be clear, precise and detailed enough as it will be used to later determine if the user problems is succesfully solved. 
"""
# may combine goal_formation and task_lister into 1 subgraph
def goal_formation(state: State):
    
    prompt = [SystemMessage(content=goal_formation_prompt)] + [state["messages"][-1]]
    response = llm.invoke(prompt)
    goal = TasksPlanning(goal=str(response.content), tasks="")

    return {"tasks_planning": goal}

task_lister_prompt = """
Given the query and the main goal, list out detailed tasks and subtasks that need to be done to answer the query efficiently with absolute perfection.
You will have access to a SQL database. You can query the database and fetch the data you need.
Goal: {goal}

Example Output Format:
DB related task:-
Task 1: Do something
Task 2: Do something

Non DB related task:-
Task 1: Do something
Task 2: Do something
...
"""
def task_lister(state: State):
    goal = state["tasks_planning"].goal # type: ignore || check later
    prompt = [SystemMessage(content=task_lister_prompt.format(goal=goal))] + [state["messages"][-1]]
    response = llm.invoke(prompt)
    state["tasks_planning"] = TasksPlanning(goal=goal, tasks=str(response.content), current_task=0)

    return {"tasks_planning": state["tasks_planning"]}

# db_master_prompt = """
# Given the query and the main goal, list out detailed tasks and subtasks (in chronological order) that need to be done to answer the query efficiently with absolute perfection.
# Goal: {goal}

# Example Output Format:
# Task 1: Do something
# Subtask 1.1: Do something
# Subtask 1.2: Do something
# Task 2: Do something
# ...
# """
# def db_master(state: State):
#     goal = state["tasks_planning"].goal # type: ignore || check later
#     prompt = [SystemMessage(content=db_master_prompt.format(goal=goal))] + [state["messages"][-1]]
#     response = llm_with_tools.invoke(prompt)
    
#     return {"messages": [response]}

# def db_master_call(state: State) -> Literal["db_master", "assistant"]:
#     return "assistant"

# not yet implemented
assistant_prompt = """
Main Goal: {goal}
Tasks: 
{tasks}

"""
system_msg = "You are the master of the agentic system. Given the tasks and goals, complete the task efficiently. Whatever happens you should do the task 1 at a time."
def assistant(
        state: State,
        config: RunnableConfig,
        store: BaseStore
):
    goal = state["tasks_planning"].goal 
    tasks = state["tasks_planning"].tasks

    prompt = [SystemMessage(content=assistant_prompt.format(goal=goal, tasks=tasks))] + [state["messages"][-1]]
    # query = state["messages"][-1].content
    pass

    # response = llm_with_tools.invoke([system_msg] + state["tasks"])
    
    # return {"messages": [response]}




# temp_sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
# def temp_assistant(
#         state: State,
#         config: RunnableConfig,
#         store: BaseStore):
   
#    # get user_id
#         # user_id = config["configurable"]["user_id"] # type: ignore
#         user_id = "test_user_id" # likely have only 1 user, so stick with hardcode user id
#         namespace = ("memories", user_id)

#         memories = store.search(namespace, query=str(state["messages"][-1].content))
#         info = "\n".join([d.value["data"] for d in memories])

#         # Store new memories if the user asks the model to remember
#         last_message = state["messages"][-1]
#         if "remember" in last_message.content.lower(): # type: ignore
#             memory = "User name is Bob"
#             # highlight-next-line
#             store.put(namespace, str(uuid.uuid4()), {"data": memory})
            

#         # response = model.invoke(
#         #     [{"role": "system", "content": system_msg}] + state["messages"]
#         # )
#         # return {"messages": response}

#         human_message = state["messages"][-1]
#         response_content = f"You said: '{human_message.content}'. I am an AI chatbot."

#         return {"messages": [AIMessage(content=response_content)]}

#    return {"messages": [llm_with_tools.invoke([temp_sys_msg] + state["messages"])]}
    # pass
