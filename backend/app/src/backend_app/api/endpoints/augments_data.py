from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from backend_app.core.model_to_dict import model_to_dict
from shared.database import AsyncSessionDep
from shared.models.augments import Augment

router = APIRouter()

@router.get("/augments_data")
async def get_augments_data(
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    augments = (await session.scalars(select(Augment))).all()
    to_serialize = [model_to_dict(augment) for augment in augments]
    
    return to_serialize