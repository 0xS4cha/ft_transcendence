from fastapi import APIRouter, HTTPException

from backend_app.core.authenticate import Authenticate
from backend_app.core.security import Password
from backend_app.database import AsyncSessionDep
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserCreate, UserPublic

router = APIRouter()

@router.post("/", response_model=UserPublic)
async def signup(
    user_data: UserCreate,
    session: AsyncSessionDep
):
    user = await Authenticate.get_user(user_data.email, session)

    if user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=409, detail="Passwords must match")

    new_user = UserModel(
        email=user_data.email,
        hashed_password=Password.hash_password(user_data.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user