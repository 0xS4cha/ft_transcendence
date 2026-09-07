from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend_app.core.security import password
from backend_app.database import AsyncSessionDep
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserCreate, UserPublic, UserLogin

router = APIRouter()

@router.post("/signup", response_model=UserPublic)
async def signup(
    user_data: UserCreate,
    session: AsyncSessionDep
):
    existing_user = await session.scalar(
        select(UserModel).where(UserModel.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=409, detail="Passwords must match")

    user = UserModel(
        email=user_data.email,
        hashed_password=password.hash_password(user_data.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@router.post("/login", response_model=UserPublic)
async def login(
    user_data: UserLogin,
    session: AsyncSessionDep
):
    existing_user = await session.scalar(
        select(UserModel).where(UserModel.email == user_data.email)
    )

    if not existing_user:
        raise HTTPException(status_code=409, detail="Email doesn't exist")

    hashed_password = await session.scalar(
        select(UserModel.hashed_password).where(UserModel.email == user_data.email)
    )

    valid_password = password.verify_password(
        user_data.password,
        hashed_password
    )

    if not valid_password:
        raise HTTPException(status_code=409, detail="Incorrect password")

    