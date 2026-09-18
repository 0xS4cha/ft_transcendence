from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from shared.database import AsyncSessionDep
from shared.models.items import Item
from backend_app.core.model_to_dict import model_to_dict

router = APIRouter()

@router.get("/items_data")
async def get_items_data(
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    items = (await session.scalars(select(Item))).all()
    to_serialize = [model_to_dict(item) for item in items]
    
    return to_serialize