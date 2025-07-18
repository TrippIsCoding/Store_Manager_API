from fastapi import FastAPI
from database import Base, engine
from manager_crud import manager_router

app = FastAPI()
app.include_router(manager_router)

Base.metadata.create_all(bind=engine)
