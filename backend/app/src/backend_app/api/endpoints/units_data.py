from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from backend_app.core.model_to_dict import model_to_dict
from shared.database import AsyncSessionDep
from shared.models.units import Unit

router = APIRouter()

@router.get("/units_data")
async def get_units_data(
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    units = (await session.scalars(select(Unit))).all()
    to_serialize = [model_to_dict(unit) for unit in units]
    
    return to_serialize