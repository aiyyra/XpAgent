from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition # a temp toolnode for test

# from utils.state import State, InputState
from agent.utils.state import TestState as State # a temp state for test
from agent.utils.nodes import test_llm, assistant
from agent.utils.test_tools import tools # a temp tool for test

# use checkpoints and store that connects to the database.

overall_workflow = (
    StateGraph(State)
    .add_node("assistant", assistant)
    .add_node("tools", ToolNode(tools))
    

    .add_edge(START, "assistant")
    .add_conditional_edges(
        "assistant",tools_condition
    )
    .add_edge("tools", "assistant")
)

graph = overall_workflow.compile()