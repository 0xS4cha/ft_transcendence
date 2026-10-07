from typing import Annotated
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from backend_app.schemas.user import UserPublic
from backend_app.models.users import UserModel
from backend_app.core.jwt import Token
from shared.database import AsyncSessionDep
from sqlalchemy import update
from backend_app.services.process_img import ProcessImg, ProcessImgMediaTypeError, ProcessImgBadRequestError, ProcessImgPayloadError, ProcessImgStorageError, remove_file
from fastapi.concurrency import run_in_threadpool


router = APIRouter()

@router.post(
    "/change_picture",
    response_model=UserPublic
)
async def change_picture(
    session: AsyncSessionDep,
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    file: UploadFile = File(),
) -> UserModel:

    process = ProcessImg()
    try:
        image_id = await run_in_threadpool(process.process_profile_pic, file.file)
    
    except ProcessImgPayloadError as e:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(e)
        )
    except ProcessImgMediaTypeError as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(e)
        )
    except ProcessImgBadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ProcessImgStorageError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    old_picture = current_user.picture
    picture = f"profile_pictures/{image_id}.webp"
    path = os.path.join("/app/src/shared", picture)

    try:
        result = await session.execute(
            update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(picture=picture)
            .returning(UserModel.id)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await session.commit()

    except Exception:
        await session.rollback()
        remove_file(path)
        raise
    
    if old_picture and not old_picture.startswith("https://cdn.intra.42.fr/users/"):
        old_path = os.path.join("/app/src/shared", old_picture)
        remove_file(old_path)
        
    await session.refresh(current_user)
    
    return current_user