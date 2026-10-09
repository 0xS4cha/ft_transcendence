from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from backend_app.core.authenticate import Authenticate
from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserCreate, UserPublic
from shared.database import AsyncSessionDep

router = APIRouter()


@router.post("/signup", response_model=UserPublic)
async def signup(
    user_data: UserCreate,
    session: AsyncSessionDep,
    response: Response,
):
    if (
        await Authenticate.get_user(user_data.email, session)
        or await Authenticate.username_taken(user_data.username, session)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username is already taken",
        )

    new_user = UserModel(
        email=user_data.email,
        hashed_password=Password.hash_password(user_data.password),
        username=user_data.username,
        picture=None,
        email_verified=False,
    )
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username is already taken",
        ) from None

    await session.refresh(new_user)
    Token.generate_token(new_user, response)
    return new_user