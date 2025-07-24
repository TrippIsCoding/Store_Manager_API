from fastapi import FastAPI
from shared_files.database import Base, engine
from User_API.auth import auth_router
from User_API.customer_crud import customer_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(customer_router, prefix='/customer', tags=['customer'])

Base.metadata.create_all(bind=engine)
