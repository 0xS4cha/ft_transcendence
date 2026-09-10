from fastapi import APIRouter
from sqlalchemy import inspect, select
from sqlalchemy.orm import selectinload

from shared.database import AsyncSessionDep
from shared.models.champions import Champion

router = APIRouter()

def sqlalchemy_to_dict(obj, visited=None):
    if visited is None:
        visited = set()

    if obj is None:
        return None

    obj_key = (type(obj), id(obj))
    if obj_key in visited:
        return None

    visited.add(obj_key)
    mapper = inspect(obj).mapper
    state = inspect(obj)
    data = {
        column.key: getattr(obj, column.key)
        for column in mapper.column_attrs
    }

    for relationship in mapper.relationships:
        if relationship.key not in state.unloaded:
            value = getattr(obj, relationship.key)

            if value is None:
                data[relationship.key] = None

            elif relationship.uselist:
                data[relationship.key] = [
                    sqlalchemy_to_dict(item, visited)
                    for item in value
                ]
            else:
                data[relationship.key] = sqlalchemy_to_dict(
                    value, visited
                )
    return data


@router.get("/{champion_id}")
async def get_champion(champion_id: int, session: AsyncSessionDep):    
    async with session.begin():
        stmt = (
            select(Champion)
            .where(Champion.id == champion_id)
            .options(
                selectinload(Champion.tactical_info),
                selectinload(Champion.playstyle_info),
                selectinload(Champion.tag_info),
                selectinload(Champion.passive),
                selectinload(Champion.roles),
                selectinload(Champion.recommended_item_defaults),
                selectinload(Champion.skins),
                selectinload(Champion.spells),
            )
        )

        result = await session.execute(stmt)
        champion = result.scalar_one_or_none()
    
        if champion:
            return sqlalchemy_to_dict(champion)
        return {'status': 'not found'}
