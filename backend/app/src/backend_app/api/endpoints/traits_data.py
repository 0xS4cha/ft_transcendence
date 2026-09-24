from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from backend_app.core.model_to_dict import model_to_dict
from shared.database import AsyncSessionDep
from shared.models.traits import Trait

router = APIRouter()

@router.get("/traits_data")
async def get_traits_data(
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    traits = (await session.scalars(select(Trait))).all()
    to_serialize = [model_to_dict(trait) for trait in traits]
    
    return to_serialize