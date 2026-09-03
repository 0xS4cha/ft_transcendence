from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend_app.core.security import hash_password
from backend_app.database import AsyncSessionDep
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserCreate, UserPublic

router = APIRouter() 

@router.post("/signup", response_model=UserPublic)
async def signup(
    user_data: UserCreate,
    db: AsyncSessionDep
):
    existing_user = await db.scalar(
        select(UserModel).where(UserModel.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=409, detail="Passwords must match")

    user = UserModel(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user