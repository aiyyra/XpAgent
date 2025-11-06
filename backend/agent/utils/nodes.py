import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage


from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

from agent.utils.state import TestState  as State
from agent.utils.test_tools import tools

# Define Chat Model
llm = ChatOpenAI(model="gpt-4", temperature=0.0)
llm_with_tools = llm.bind_tools(tools)


# This is a test node to try our structure first. It will not be part of the final code.
def test_llm(state: State):

    # return some message or function of the node
    pass

temp_sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
def assistant(
        state: State,
        config: RunnableConfig,
        store: BaseStore):
   
   # get user_id
        # user_id = config["configurable"]["user_id"] # type: ignore
        user_id = "test_user_id" # likely have only 1 user, so stick with hardcode user id
        namespace = ("memories", user_id)

        memories = store.search(namespace, query=str(state["messages"][-1].content))
        info = "\n".join([d.value["data"] for d in memories])

        # Store new memories if the user asks the model to remember
        last_message = state["messages"][-1]
        if "remember" in last_message.content.lower(): # type: ignore
            memory = "User name is Bob"
            # highlight-next-line
            store.put(namespace, str(uuid.uuid4()), {"data": memory})
            

        # response = model.invoke(
        #     [{"role": "system", "content": system_msg}] + state["messages"]
        # )
        # return {"messages": response}

        human_message = state["messages"][-1]
        response_content = f"You said: '{human_message.content}'. I am an AI chatbot."

        return {"messages": [AIMessage(content=response_content)]}

#    return {"messages": [llm_with_tools.invoke([temp_sys_msg] + state["messages"])]}
    # pass