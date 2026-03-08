import os

import dotenv

dotenv.load_dotenv(".env")


class Config:
    API_PATH = os.getenv("API_PATH")
    API_KEY = os.getenv("API_KEY")
    DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    DEBUG = False if os.getenv("DEBUG") == 0 else True
