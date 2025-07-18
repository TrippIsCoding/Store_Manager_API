from fastapi import APIRouter, Depends, HTTPException
from models import UpdateItemModel, ItemModel, Item
from sqlalchemy.orm import session
from database import get_db

manager_router = APIRouter(prefix='/inventory')

@manager_router.get('/view')
async def view_inventory(db: session = Depends(get_db)):
    inventory = db.query(Item).all()

    return ({'id': item.id, 'name': item.name, 'price': item.price, 'in_stock': item.in_stock} for item in inventory)

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

    return {'message': 'The item was added to the inventory.'}

@manager_router.put('/update/{id}')
async def update_item(id: int, updated_item: UpdateItemModel = Depends(), db: session = Depends(get_db)):
    item = db.query(Item).filter(Item.id==id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f'Item {id} could not be found.')

    item.price = updated_item.price
    item.in_stock = updated_item.in_stock

    db.commit()
    db.refresh(item)

    return {'id': item.id, 'message': f'Item {item.name} has been updated with the provded info.'}

@manager_router.delete('/delete/{id}')
async def delete_item(id: int, db: session = Depends(get_db)):
    item = db.query(Item).filter(Item.id==id).first()

    db.delete(item)
    db.commit()

    return {'message': 'Item was removed.'}