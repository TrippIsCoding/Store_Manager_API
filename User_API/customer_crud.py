from fastapi import APIRouter, HTTPException, Depends
from shared_files.database import get_db, r
from sqlalchemy.orm import session
from shared_files.models import Item
from User_API.auth import oauth2_scheme, verify_token
import json

def get_cart_key(username: str, id: int):
    return f'cart:{username}_{id}'

customer_router = APIRouter()

@customer_router.get('/view/store')
async def view_store(db: session = Depends(get_db)):
    inventory = db.query(Item).all()

    if not inventory:
        raise HTTPException(status_code=404, detail="There are no items in inventory right now. Please come back later.")
    
    return [{'name': item.name, 'price': f'${item.price}', 'in_stock': item.in_stock} for item in inventory]

@customer_router.post('/cart/add/{id}')
async def add_to_cart(id: int, token: str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    user_info = verify_token(token)
    cart_key = get_cart_key(user_info['sub'], user_info['user_id'])

    item = db.query(Item).filter(Item.id==id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f'There is no item with the id: {id}')

    try:
        if existing_item := r.hget(cart_key, item.id):
            item_info = json.loads(existing_item)
            item_info['quantity'] = item_info.get('quantity', 1) + 1

        else:
            item_info = {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'quantity': 1
            }

        r.hset(cart_key, item.id, json.dumps(item_info))
        r.expire(cart_key, 86400)
    except:
        raise HTTPException(status_code=500, detail=f'There was a problem adding {item.name} to cart. Please try again later.')
    
    return {'message': f'Item: {item.name} was added to cart!'}

@customer_router.get('/cart/view')
async def view_cart(token: str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    user_info = verify_token(token)
    cart_key = get_cart_key(user_info['sub'], user_info['user_id'])

    cart = r.hgetall(cart_key)

    return [json.loads(cart[id]) for id in cart]

@customer_router.delete('/cart/delete/{id}')
async def remove_item_from_cart(id: int, token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    cart_key = get_cart_key(user_info['sub'], user_info['user_id'])

    item = json.loads(r.hget(cart_key, id))

    try:
        if item['quantity'] > 1:
            item['quantity'] = item.get('quantity', 1) - 1
            r.hset(cart_key, id, json.dumps(item))
        else:
            r.hdel(cart_key, id)
    except:
        raise HTTPException(status_code=500, detail='Could not delete item from the cart. Please try again later.')

    return {'message': f'The item was removed from your cart.'}
