from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
from shared_files.models import User, UserModel 
from shared_files.database import get_db
from shared_files.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/user/login')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def verify_token(token: str):
    '''
    verify_token verifies the users jwt if its not a valid jwt it raises a 401 status code 
    this function also return the decoded jwt so i can get user info like user id and username from it
    '''
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail='User is unauthorized')

# below is the code for the auth endpoints
auth_router = APIRouter()

@auth_router.post('/user/signup')
async def create_account(user: User, db: Session = Depends(get_db)):
    '''
    create_account allows users to sign up storing thier username, password, email, and full name in the database for future login
    '''
    try:
        validate_email(user.email)
    except EmailNotValidError: 
        raise HTTPException(status_code=422, detail='Invalid email address')

    new_user = UserModel(
        username=user.username,
        password=hash_password(user.password),
        email=user.email,
        full_name=user.full_name,
        address=user.address # can't add address validation without relying on an api so i'm not adding it
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Username or email already in use')

    return {'user': new_user}

@auth_router.post('/user/login')
async def user_authenticate(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    user_authenticate returns a jwt if the user info is valid
    '''
    user_info = db.query(UserModel).filter(UserModel.username==user.username).first()
    if not user_info:
        raise HTTPException(status_code=404, detail='User not found in database')
    if not verify_password(user.password, user_info.password):
        raise HTTPException(status_code=401, detail='password is incorrect')
    
    payload = {'user_id': user_info.id, 'sub': user_info.username, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)}
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {'token': token}
