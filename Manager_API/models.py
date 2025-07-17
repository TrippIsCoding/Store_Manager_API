from sqlalchemy import String, Integer, Float, Column
from pydantic import BaseModel, Field
from typing import Annotated
from database import Base

class ItemModel(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=80)]
    price: Annotated[float, Field(le=100000, ge=.01)]
    in_stock: Annotated[int, Field(ge=1, le=100000)]

class Item(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    price = Column(Float)
    in_stock = Column(Integer, index=True)

