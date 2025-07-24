from sqlalchemy import String, Integer, Float, Column
from pydantic import BaseModel, Field
from typing import Annotated
from shared_files.database import Base

class UpdateItemModel(BaseModel):
    price: Annotated[float, Field(le=100000, ge=.01)]
    in_stock: Annotated[int, Field(ge=1, le=100000)]

class ItemModel(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=80)]
    price: Annotated[float, Field(le=100000, ge=.01)]
    in_stock: Annotated[int, Field(ge=1, le=100000)]

class Item(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    price = Column(Float)
    in_stock = Column(Integer, index=True)

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    email = Column(String, index=True, unique=True)
    full_name = Column(String, nullable=True)
    address = Column(String)


class User(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=8, max_length=72)]
    email: Annotated[str, Field(max_length=100)]
    full_name: Annotated[str, Field(max_length=100)] | None = None
    address: Annotated[str, Field(min_length=5, max_length=250)] 

    class Config:
        from_attributes = True