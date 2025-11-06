""" API v1 configuration. All api endpoints and routers are defined here. """

from fastapi import APIRouter, Body

from app.services.database import DatabaseService
from app.services.graph import GraphService
from app.schema.thread import MessageRequest, ThreadResponse

api_router = APIRouter()
db_service = DatabaseService()
graph_service = GraphService()

# may include other routers here
# api_router.include_router(other_router, prefix="/other")

# or can consider populate everything here


@api_router.post("/thread/{thread_id}/query")
async def post_message(thread_id: str, request: MessageRequest):
    """ Post message to thread. """
    reply = await graph_service.send_message_to_agent(thread_id, request.query)

    return reply

# api to get thread message history by thread id
@api_router.get("/thread/{thread_id}")
async def get_thread(thread_id: str):
    """ Get thread message history. """
    # Get thread from database in threads table
    thread = await graph_service.get_past_messages(thread_id)
    # return { "messages_history": thread }
    return thread[0]["messages"]


# api to get all threads
@api_router.get("/threads")
async def get_threads():
    """ Get all threads. """
    # Get all threads from database in threads table
    threads = []

    # return threads
    return {"message": "Hello World"} # not implemented yet

# api to create thread with uuid
@api_router.post("/thread")
async def create_thread():
    """ Create thread. """
    new_thread = db_service.new_thread()
    # Create thread in database in threads table
    return ThreadResponse(session_id=new_thread.id)

# general health check
@api_router.get("/health")
async def health_check():
    """ Health check endpoint of v1. """
    return {"status": "v1 is ok"}