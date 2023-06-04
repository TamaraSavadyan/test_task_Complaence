from fastapi import APIRouter, Depends, File, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database import get_db
from schemas import Token, UserCreate, UserResponse
from models import User
from utils import verify
from oauth2 import create_access_token

router = APIRouter(
    prefix = "/users",
    tags=['Users'],
)

@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)): 
   
    user = await db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    access_token = create_access_token(data = {"user_id": user.id})

    user.is_authorized = True
    await db.commit()

    return {"access_token": access_token, 
            "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def createUser(user: UserCreate, db: AsyncSession = Depends(get_db)):

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())

    await db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

async def check_user_authorization(id: int, db: sessionmaker):
    user = await db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not found")

    if not user.is_authorized:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with id {id} is not authorized")

    return user


@router.get("/{id}", response_model=UserResponse)
async def getUser(id: int, user: User = Depends(check_user_authorization)):
    return user