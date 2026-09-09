import time
from datetime import datetime, timedelta
from uuid import uuid4

import pytz
from fastapi import APIRouter, Response, status
from shared.models.unit_games import ProcessedGame
from sqlalchemy import func, select

from backend_app.database import AsyncSessionDep
from backend_app.models.user import UserModel
from backend_app.models.visit import VisitModel

router = APIRouter()
REFRESH_DELTA_SECONDS    = 3

stats_cache = {}
async def get_cache(name, calc_function, session: AsyncSessionDep, force_update = False):
    if name in stats_cache and not force_update:
        return stats_cache.get(name)
    stats_cache[name] = await calc_function(session)
    return stats_cache[name]


async def processed_game_calc(session: AsyncSessionDep):
    total = int(await session.scalar(select(func.count()).select_from(ProcessedGame))) or 0
    return {'count': total}

async def created_accounts(session: AsyncSessionDep):
    total = int(await session.scalar(select(func.count()).select_from(UserModel))) or 0
    return {'count': total}

async def visits(session: AsyncSessionDep):
    today = datetime.now(tz=pytz.utc).isoformat()
    session.add(
        VisitModel(
            id=uuid4().hex,
            date=today,
        )
    )
    await session.commit()
    # return count
    return [
        int(await session.scalar(
            select(func.count())
            .select_from(VisitModel)
            .where(VisitModel.date == (datetime.now(tz=pytz.utc) - timedelta(days=i)).isoformat())
        ) or 0) for i in range(10)
    ]

async def default(session: AsyncSessionDep):
    return {'count': 0}

endpoints = {
    "processed_game": {"cache": True, "function": processed_game_calc, "last": 0.0},
    "accounts_created": {"cache": False, "function": created_accounts, "last": 0.0},
    "visits": {"cache": False, "function": visits, "last": 0.0},
}
@router.get("/{name}")
async def stats_dispatcher(name: str, response: Response, session: AsyncSessionDep):
    if name in endpoints:
        force_update = time.time() - endpoints[name].get("last", 0) > REFRESH_DELTA_SECONDS
        if endpoints[name].get("cache", False) is True:
            result = await get_cache(name, endpoints[name].get("function", default), session, force_update)
        else:
            result = await endpoints[name].get("function", default)(session)
        if force_update:
            endpoints[name]["last"] = time.time()
        return result
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'success': False}
