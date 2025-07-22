from fastapi import APIRouter, HTTPException, Depends
from shared_files.database import get_db, r
from sqlalchemy.orm import session

customer_router = APIRouter()

@customer_router.get('/')
async def view_store(db: session = Depends(get_db)):
    
