#main to test our graph 
# from agent.utils.test_tools import tools
# print(tools[0](1,2))
from langchain_core.messages import HumanMessage

# repair path. Not sure why this happen
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# load api key
from dotenv import load_dotenv
load_dotenv()

# from langchain_core.messages import HumanMessage
# from agent.graph.db_master_graph import db_master


# # test current graph
# messages = [HumanMessage(content="list 3 actors and movies")]
# messages = db_master.invoke({"messages": messages}) # type: ignore

# # config = {"configurable": {"thread_id": "1", "user_id": "1"}}

# config = {
#     "configurable": {
#         "thread_id": "1",
#         # "checkpoint_id": "1f0b2f5f-a9a1-6e59-bfff-97132a908f861",
#         # "user_id": "1",
#     }
# }

# state = db_master.get_state(config) # type: ignore

# print(state)
# for m in messages['messages']:
#     m.pretty_print()

# Result: This structure works
from agent.src.build_graph import graph_construction

chain = graph_construction("gpt-4o", 0.2, "agent/data/art.db", "logs/")

question: str = "Find only 2 paintings that start with the letter A, Then find only 1 that starts with the letter T"

config = {"configurable": {"thread_id": "m2ex-dev"}}
messages = [HumanMessage(content=question)]
messages = chain.invoke({"messages": messages}, config=config) # type: ignore
for m in messages['messages']:
    m.pretty_print()
