import os
from uuid import uuid4
from sqlmodel import Field, SQLModel, create_engine, Session, select

from app.core.config import settings
from app.models.thread import Thread


# Class DatabaseService()
# Handle database initialization (helps to maintain one instance of database throughout the app)
# has all functions to interact with database
# Will only interact with thread and messages models

# functionality (stick with sync function first)

# thread
# create thread
# get thread and all of its messages
# delete thread and all its messages
# list all thread

# messages
# create message
# delete message
# update message (optional, dont do it first)

class DatabaseService():
    def __init__(self):
        self.engine = create_engine(settings.DB_URI, echo=True) # type: ignore
        # Create all tables if not created, can comment after done initialize
        SQLModel.metadata.create_all(self.engine)

    def new_thread(self, ) -> Thread:
        with Session(self.engine) as session:
            thread = Thread(id=str(uuid4()))
            session.add(thread)
            session.commit()
            session.refresh(thread)
            return thread

    def get_all_thread(self) -> list[Thread]:
        with Session(self.engine) as session:
            # threads = session.query(Thread).all()
            statement = select(Thread)
            threads = session.exec(statement).all()
            return threads # type: ignore


database_service = DatabaseService()
