import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .services.database import DatabaseService
from .models.message import Message
from .models.thread import Thread

from .api.v1.api import api_router

from dotenv import load_dotenv
load_dotenv()


# db_service = DatabaseService()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],# this is the dev frontend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint
    """
    db_uri = os.getenv("DB_URI")
    # db_service = DatabaseService() # test here just to create the table, remove later
    return {"message": db_uri}

@app.get("/health")
async def health():
    """
    Health check endpoint.

    Check database health
    """
    return {"message": "OK, did not implement database check yet"}

# @app.get("/test_agent")
# def test_agent():
#     """
#     Test Agent endpoint.

#     Check Agent response. Only use for testing. remove later.
#     """
#     from .services.graph import test_agent

#     response = test_agent("Remember Bob")

#     return {"retrieved": response[0].content}

