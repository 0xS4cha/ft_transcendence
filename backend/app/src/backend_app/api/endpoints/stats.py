from fastapi import APIRouter
from shared.models import UnitStat
from backend_app.database import AsyncSessionDep
from sqlalchemy import select, func
from fastapi import Response, status


router = APIRouter()

stats_cache = {}
async def get_cache(name, calc_function, session: AsyncSessionDep):
    if name in stats_cache:
        return stats_cache.get(name)
    stats_cache[name] = calc_function(session)


async def processed_game_calc(session: AsyncSessionDep):
    total = await session.scalar(select(func.sum(UnitStat.count))) or 0
    return {"count": total}

async def default(session: AsyncSessionDep):
    return 0

endpoints = {
    "processed_game": {"cache": True, "function": processed_game_calc}
}
@router.get("/{name}")
async def stats_dispatcher(name: str, response: Response, session: AsyncSessionDep):
    if name in endpoints.keys():
        #if endpoints[name].get("cache", False):
        #    return await get_cache(name, endpoints[name].get("function", default))
        #else:
        return await endpoints[name].get("function", default)(session)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'success': False}
