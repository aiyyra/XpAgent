# This will be where we import the graph from our actual agent package
# Compile graph here and use checkpoint and store for our database
# Get db connection string from settings in config 
import os

from langchain_core.messages import HumanMessage

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

from langgraph.graph import StateGraph, START, END

from agent.graph.db_master_graph import builder as db_master
from agent.utils.nodes import assistant, goal_formation, task_lister
# from agent.utils.state import TestState as State
from agent.utils.state import State

class GraphService:
    def __init__(self):
        self.db_uri = str(os.getenv("DB_URI"))
        self.store = PostgresStore.from_conn_string(self.db_uri)
        self.checkpointer = PostgresSaver.from_conn_string(self.db_uri)


    def main_builder(self, checkpointer: PostgresSaver, store: PostgresStore):
        m_builder = (
            StateGraph(State)
            .add_node("goal_formation", goal_formation)
            .add_node("task_lister", task_lister)
            # .add_node("assistant", assistant)
            
            # .add_conditional_edges("db_master", db_master.compile(checkpointer=checkpointer, store=store))
            # .add_node("db_master", db_master.compile(checkpointer=checkpointer, store=store))

            .add_edge(START, "goal_formation")
            .add_edge("goal_formation", "task_lister")
            # .add_edge("task_lister", "assistant")
            # .add_edge("assistant", "db_master")
            # .add_edge("db_master", "assistant")
            # .add_edge("assistant", END)

        )

        return m_builder.compile(checkpointer=checkpointer, store=store)


    
    async def send_message_to_agent(self, thread_id: str, query: str):
        with (
            PostgresStore.from_conn_string(self.db_uri) as store,
            PostgresSaver.from_conn_string(self.db_uri) as checkpointer
        ):
            config = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }

            # checkpointer.setup()
            # store.setup()
            
            graph = self.main_builder(checkpointer=checkpointer, store=store)
            
            # Invoking the graph here
            reply = graph.invoke(
                {"messages": [HumanMessage(content=query)]}, # type: ignore
                config=config # type: ignore
            )
            # states = graph.get_state(config=config) # type: ignore
            # past_messages = states.values["messages"]

            # return past_messages

            return reply
        
    async def get_past_messages(self, thread_id: str):
        with (
            PostgresStore.from_conn_string(self.db_uri) as store,
            PostgresSaver.from_conn_string(self.db_uri) as checkpointer
        ):
            config = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }
            graph = self.main_builder(checkpointer=checkpointer, store=store)
            states = graph.get_state(config=config) # type: ignore
            # past_messages = states.values["messages"]
            return states
            


# # make async with later to managed resource connection status
# def test_agent_old(query: str):
#     with (
#         PostgresStore.from_conn_string(str(DB_URI)) as store,
#         PostgresSaver.from_conn_string(str(DB_URI)) as checkpointer
#     ):
        
#         config = {
#                 "configurable": {
#                     # highlight-next-line
#                     "thread_id": "1",
#                     # "user_id": "1"
#                 }
#             }
        
#         graph = overall_workflow.compile(checkpointer=checkpointer, store=store)

#         # test invoke here
#         # graph.invoke(
#         #     {"messages": [HumanMessage(content=query)]}, # type: ignore
#         #     config=config # type: ignore
#         # )

#         # test getting states from checkpointer here
#         states = graph.get_state(config=config) # type: ignore
#         past_messages = states.values["messages"]
        
#     return past_messages

    
# # Sending message to agent
# def send_message_to_agent(query: str, thread_id: str):
#     with (
#         PostgresStore.from_conn_string(str(DB_URI)) as store,
#         PostgresSaver.from_conn_string(str(DB_URI)) as checkpointer
#     ):
#         config = {
#                 "configurable": {
#                     # highlight-next-line
#                     "thread_id": thread_id,
#                 }
#             }
#         graph = overall_workflow.compile(checkpointer=checkpointer, store=store)
#         reply = graph.invoke(
#             {"messages": [HumanMessage(content=query)]}, # type: ignore
#             config=config # type: ignore
#         )
#     return reply