from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from shared_files.config import DATABASE_URL, REDIS_HOST_URL, REDIS_PASSWORD
import redis

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

r = redis.Redis(host=REDIS_HOST_URL, port=13001, decode_responses=True, username='default', password=REDIS_PASSWORD)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
