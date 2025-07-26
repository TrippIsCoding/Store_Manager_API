import os
from dotenv import load_dotenv

if os.getenv('RENDER') != True: # this if statement is for the deployed api on render to load the env variables.
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST_URL = os.getenv("REDIS_HOST_URL")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
