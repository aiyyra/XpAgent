# Get all env and config here
import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):

        load_dotenv()

        self.DB_URI = os.getenv("DB_URI") 
        self.AGENT_DB_URI = os.getenv("TARGET_DB_URI")

settings = Settings()
