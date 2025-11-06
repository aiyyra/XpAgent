import uuid
import dotenv
dotenv.load_dotenv()

from langgraph.graph import StateGraph
from langgraph.graph.message import MessagesState  
from langchain_core.messages import AIMessage
from langgraph.graph import START

# from langfuse.langchain import CallbackHandler
 
# langfuse_handler = CallbackHandler()

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
 
# llm = ChatOpenAI(model="gpt-4o")
# prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
# chain = prompt | llm
 
# response = chain.invoke(
#     {"topic": "cats"}, 
#     config={"callbacks": [langfuse_handler]})

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore


DB_URI = "postgresql://postgres:postgres@192.168.0.3:5432/playground"
# highlight-next-line
with (
    PostgresStore.from_conn_string(DB_URI) as store,
    PostgresSaver.from_conn_string(DB_URI) as checkpointer
):
    builder = StateGraph(MessagesState)

    # def temp basic node with message state
    def chatbot_node(
            state: MessagesState,
            config: RunnableConfig,

            store: BaseStore
            ) -> MessagesState:
        
        # get user_id
        user_id = config["configurable"]["user_id"] # type: ignore
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


    # Add node
    builder.add_node("node_1", chatbot_node)

    # Add edge
    builder.add_edge(START, "node_1")

    # highlight-next-line
    graph = builder.compile(checkpointer=checkpointer, store=store)
    
    config = {
            "configurable": {
                # highlight-next-line
                "thread_id": "1",
                "user_id": "1"
            }
        }

    store.setup()
    graph.invoke({"messages": [AIMessage(content="remember bob")]}, config=config) # type: ignore