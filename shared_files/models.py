from sqlalchemy import String, Integer, Float, Column
from pydantic import BaseModel, Field
from typing import Annotated
from shared_files.database import Base

class UpdateItemModel(BaseModel):
    '''
    UpdateItemModel is for the /update/{id} endpoint in manager_crud.py so i can allow the store manager
    the ability to update a specific items information.
    '''
    price: Annotated[float, Field(le=100000, ge=.01)]
    in_stock: Annotated[int, Field(ge=1, le=100000)]

class ItemModel(BaseModel):
    '''
    ItemModel is used to help create a item in the store
    it's also being used for input validation
    '''
    name: Annotated[str, Field(min_length=2, max_length=80)]
    price: Annotated[float, Field(le=100000, ge=.01)]
    in_stock: Annotated[int, Field(ge=1, le=100000)]

class Item(Base):
    '''
    Item is a class for the sqlalchemy orm I use it to query the database and add new items.
    '''
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    price = Column(Float)
    in_stock = Column(Integer, index=True)

class UserModel(Base):
    '''
    UserModel is being used for the auth.py file in the User_API this allows me to save information
    when someone signs up allowing them to log in, in the future.
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)
    email = Column(String, index=True, unique=True)
    full_name = Column(String, nullable=True)
    address = Column(String)


class User(BaseModel):
    '''
    User is being used for input validation for the users information before adding it to the database.
    '''
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=8, max_length=72)]
    email: Annotated[str, Field(max_length=100)]
    full_name: Annotated[str, Field(max_length=100)] | None = None
    address: Annotated[str, Field(min_length=5, max_length=250)] 

    class Config:
        from_attributes = True