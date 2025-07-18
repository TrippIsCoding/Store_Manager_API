from fastapi import APIRouter, Depends, HTTPException
from models import ItemModel, Item
from sqlalchemy.orm import session
from database import get_db, r
import json

manager_router = APIRouter(prefix='/inventory')

@manager_router.get('/view')
async def view_inventory(db: session = Depends(get_db)):
    inventory = db.query(Item).filter_by(Item.id)

    return {'nothing': 'nothing'}

@manager_router.post('/add')
async def add_to_inventory(new_item: ItemModel = Depends(), db: session = Depends(get_db)):
    add_new_item = Item(
        name=new_item.name,
        price=new_item.price,
        in_stock=new_item.in_stock
    )

    db.add(add_new_item)
    db.commit()
    db.refresh(add_new_item)

    item = {
        'id': add_new_item.id,
        'name': add_new_item.name,
        'price': add_new_item.price,
        'in_stock': add_new_item.in_stock
    }

    r.set(item['name'], json.dumps(item))

    return {'message': 'The item was added to the inventory.'}
