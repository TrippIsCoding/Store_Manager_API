import os
from dotenv import load_dotenv

if os.getenv('RENDER') != True:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_HOST_URL = os.getenv("REDIS_HOST_URL")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")