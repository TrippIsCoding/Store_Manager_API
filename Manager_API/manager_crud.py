from fastapi import APIRouter, Depends, HTTPException
from shared_files.models import UpdateItemModel, ItemModel, Item
from sqlalchemy.orm import session
from shared_files.database import get_db

manager_router = APIRouter(prefix='/inventory')

@manager_router.get('/view')
async def view_inventory(db: session = Depends(get_db)):
    '''
    the /view endpoint retrieves every item in the store and returns it in a dictionary 
    example: id, name, price, in_stock
    '''
    inventory = db.query(Item).all()

    if not inventory:
        raise HTTPException(status_code=404, detail='There are curerntly no items in inventory. Come back later.')

    return [{'id': item.id, 'name': item.name, 'price': item.price, 'in_stock': item.in_stock} for item in inventory]

@manager_router.post('/add')
async def add_to_inventory(new_item: ItemModel, db: session = Depends(get_db)):
    '''
    the /add endpoint allows the store manager to add items to the stores inventory which can then be viewed by customers.
    '''
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
async def update_item(id: int, updated_item: UpdateItemModel, db: session = Depends(get_db)):
    '''
    the /update/{id} endpoint allows the store manager to update an existing items price and the amount in stock whenever they want.
    '''
    item = db.query(Item).filter(Item.id==id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f'Item {id} not found.')

    item.price = updated_item.price
    item.in_stock = updated_item.in_stock

    db.commit()
    db.refresh(item)

    return {'id': item.id, 'message': f'Item {item.name} has been updated with the provded info.'}

@manager_router.delete('/delete/{id}')
async def delete_item(id: int, db: session = Depends(get_db)):
    '''
    the /delete/{id} endpoint allows the store manager to delete an existing item from the stores inventory.
    '''
    item = db.query(Item).filter(Item.id==id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f'Item {id} not found')

    db.delete(item)
    db.commit()

    return {'message': 'Item was removed.'}