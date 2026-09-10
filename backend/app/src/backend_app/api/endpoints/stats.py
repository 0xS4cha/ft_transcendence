import time
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Response, status
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from backend_app.models.user import UserModel
from backend_app.models.visit import VisitModel
from shared.database import AsyncSessionDep
from shared.models.unit_games import PerDayStats, ProcessedGame

router = APIRouter()
REFRESH_DELTA_SECONDS    = 3
VISITOR_LIST_RANGE_DAY   = 90

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

async def get_per_day_stats(session: AsyncSessionDep):
    today = datetime.now(UTC).date()
    per_day_stats: list[PerDayStats] = (await session.scalars(select(PerDayStats))).all()
    
    return {
        'total': {
            "gold_wasted": sum([s.goldWasted for s in per_day_stats]),
            "total_game_length": sum([s.totalGameLength for s in per_day_stats]),
            "total_games": sum([s.totalGames for s in per_day_stats]),
        },
        'daily': [
            {
                "date": str(today - timedelta(days=i)),
                "gold_wasted_avg": (per_day_stats[i].goldWasted / per_day_stats[i].totalGames) if per_day_stats[i].totalGames > 0 else 0,
                "time_elapsed_avg": (per_day_stats[i].totalGameLength / per_day_stats[i].totalGames) if per_day_stats[i].totalGames > 0 else 0,
            } for i in range(VISITOR_LIST_RANGE_DAY) if i < len(per_day_stats)
        ]
    }

async def visits(session: AsyncSessionDep):
    today = datetime.now(UTC).date()

    stmt = insert(VisitModel).values(
        date=today,
        count=1,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[VisitModel.date],
        set_={
            "count": VisitModel.count + 1,
        },
    )

    await session.execute(stmt)
    await session.commit()

    total = int(
        await session.scalar(
            select(func.sum(VisitModel.count))
        )
        or 0
    )

    return {
        "count": total,
    }


async def home(session: AsyncSessionDep):
    visits_data = await visits(session)
    daily_data = await get_per_day_stats(session)

    return {
        "visitsCount": visits_data.get("count", 0),
        "goldCount": daily_data.get("total", {}).get("gold_wasted", 0),
        "matchCount": daily_data.get("total", {}).get("total_games", 0),
        "history": list(daily_data.get("daily", []))
    }


async def default(session: AsyncSessionDep):
    return {'count': 0}

endpoints = {
    "processed_game": {"cache": True, "function": processed_game_calc, "last": 0.0},
    "accounts_created": {"cache": False, "function": created_accounts, "last": 0.0},
    "visits": {"cache": False, "function": visits, "last": 0.0},
    "daily_stats": {"cache": True, "function": get_per_day_stats, "last": 0.0},
    "home": {"cache": True, "function": home, "last": 0.0},
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
