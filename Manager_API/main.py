from fastapi import FastAPI
from shared_files.database import Base, engine
from manager_crud import manager_router

app = FastAPI()
app.include_router(manager_router)

Base.metadata.create_all(bind=engine)
