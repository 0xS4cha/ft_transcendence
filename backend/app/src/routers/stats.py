from fastapi import APIRouter
from shared.models import UnitStat
from ..database import get_async_session
from sqlalchemy import inspect, select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)

stats_cache = {}
async def get_cache(name, calc_function):
    if name in stats_cache:
        return stats_cache.get(name)
    stats_cache[name] = calc_function()


async def processed_game_calc(session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        result = await session.get(UnitStat, )
        unit = result.scalar_one_or_none()
        if unit:
            return {unit}
        return {'status': 'not found'}


endpoints = {
    "processed_game": {"cache": True, "function": processed_game_calc}
}
@router.get("/{name}")
async def stats_dispatcher(name: str):
    if name in endpoints.keys():
        if endpoints[name].get("cache", False):
            return await get_cache(name, endpoints[name].get("function", lambda: 0))
        else:
            return await endpoints[name].get("function", lambda: 0)
    return {'success': False}
