import logging
import time
from datetime import UTC, datetime, timedelta

import redis.asyncio as redis
import requests
from fastapi import APIRouter, Request, Response, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from backend_app.core.dependencies import RedisDep
from backend_app.core.rate_limiter import client_ip
from backend_app.core.websocket import WSbroadcast
from backend_app.models.chat_message import ChatMessage
from backend_app.models.users import UserModel
from backend_app.models.visit import VisitModel
from shared.database import AsyncSessionDep

logger = logging.getLogger(__name__)

router = APIRouter()
REFRESH_DELTA_SECONDS    = 3
VISITOR_LIST_RANGE_DAY   = 90
VISIT_DEDUP_SECONDS      = 2 * 24 * 3600

stats_cache = {}
async def get_cache(name, calc_function, session: AsyncSessionDep, force_update = False):
    if name in stats_cache and not force_update:
        return stats_cache.get(name)
    stats_cache[name] = await calc_function(session)
    return stats_cache[name]

tft_stats = {}
TFT_STATS_URL = "https://api.teamfight.lol/graphql"
TFT_STATS_TIMEOUT_SECONDS = 5
TFT_STATS_RETRY_SECONDS = 300
TFT_STATS_QUERY = """
query GetPlatformStats {
    getPlatformStats {
    totalSummoners
    totalMatches
    milestones {
        goldWasted
        threeStarUnits
        damageDealt
        itemsEquipped
        __typename
    }
    __typename
    }
}
"""


def fetch_graphql_tft_stats() -> None:
    try:
        response = requests.post(
            TFT_STATS_URL,
            json={
                "operationName": "GetPlatformStats",
                "query": TFT_STATS_QUERY,
                "variables": {},
            },
            timeout=TFT_STATS_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        body = response.json()
        data = body.get("data") if isinstance(body, dict) else None
        platform = (data or {}).get("getPlatformStats") or {}
        total_matches = platform.get("totalMatches")
        if total_matches is None:
            raise ValueError("missing getPlatformStats.totalMatches")
        tft_stats["total_games"] = total_matches
        tft_stats["gold_wasted"] = (platform.get("milestones") or {}).get("goldWasted", 0)
    except Exception as e:  # noqa: BLE001
        logger.warning(f"GRAPHQL STATS: Could not acquire stats for game: {e}")


async def update_graphql_tft_stats() -> None:
    now = time.time()
    if "gold_wasted" in tft_stats:
        return
    if now - tft_stats.get("_last_attempt", 0) < TFT_STATS_RETRY_SECONDS:
        return
    tft_stats["_last_attempt"] = now
    await run_in_threadpool(fetch_graphql_tft_stats)



async def created_accounts(session: AsyncSessionDep):
    total = int(await session.scalar(select(func.count()).select_from(UserModel))) or 0
    return {'count': total}

async def record_visit(session: AsyncSessionDep, r: redis.Redis, ip: str) -> None:
    today = datetime.now(UTC).date()
    try:
        first_visit_today = await r.set(f"visit:{today}:{ip}", 1, nx=True, ex=VISIT_DEDUP_SECONDS)
    except redis.RedisError:
        return
    if not first_visit_today:
        return

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


async def visits(session: AsyncSessionDep):
    today = datetime.now(UTC).date()

    total = int(
        await session.scalar(
            select(func.sum(VisitModel.count))
        )
        or 0
    )

    start_date = today - timedelta(days=VISITOR_LIST_RANGE_DAY - 1)
    result = await session.execute(
        select(VisitModel)
        .where(
            VisitModel.date >= start_date,
            VisitModel.date <= today,
        )
        .order_by(VisitModel.date.desc())
    )

    visits = result.scalars().all()
    counts = {visit.date: visit.count for visit in visits}
    history = [
        {"date": today - timedelta(days=i),
        "value": counts.get(today - timedelta(days=i), 0)}
        for i in range(VISITOR_LIST_RANGE_DAY)
    ]
    return {
        "count": total,
        "history": history
    }


async def home(session: AsyncSessionDep):
    visits_data = await visits(session)
    chat_msg_count = await session.scalar(select(func.count()).select_from(ChatMessage))

    return {
        "visitsCount": visits_data.get("count", 0),
        "chatMessagesCount": chat_msg_count,
        "goldCount": tft_stats.get("gold_wasted", 0),
        "matchCount": tft_stats.get("total_games", 0),
        "history": visits_data.get("history", [0] * VISITOR_LIST_RANGE_DAY),
    }


async def default(session: AsyncSessionDep):
    return {'count': 0}

endpoints = {
    "accounts_created": {"cache": False, "function": created_accounts, "last": 0.0},
    "visits": {"cache": False, "function": visits, "last": 0.0},
    "home": {"cache": True, "function": home, "last": 0.0},
}
@router.get("/{name}")
async def stats_dispatcher(
    name: str,
    request: Request,
    response: Response,
    session: AsyncSessionDep,
    r: RedisDep,
):
    if name not in endpoints:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'success': False}

    await update_graphql_tft_stats()
    if name in ("home", "visits"):
        await record_visit(session, r, client_ip(request))

    force_update = time.time() - endpoints[name].get("last", 0) > REFRESH_DELTA_SECONDS
    if endpoints[name].get("cache", False) is True:
        result = await get_cache(name, endpoints[name].get("function", default), session, force_update) or {}
    else:
        result = await endpoints[name].get("function", default)(session) or {}
    if force_update:
        endpoints[name]["last"] = time.time()
        if name == "home":
            await WSbroadcast("stats.update", result)
    return result
