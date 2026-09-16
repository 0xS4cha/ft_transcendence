from typing import Any

from fastapi import APIRouter
from sqlalchemy import inspect, select

from shared.database import AsyncSessionDep
from shared.models.items import Item


def model_to_dict(
        obj
) -> dict[str, Any]:
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


router = APIRouter()

@router.get("/items_data")
async def get_items_data(
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    items = (await session.scalars(select(Item))).all()
    to_serialize = [model_to_dict(item) for item in items]
    
    return to_serialize