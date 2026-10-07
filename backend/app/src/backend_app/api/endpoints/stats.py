import time
from datetime import UTC, datetime, timedelta

import requests
from backend.app.src.backend_app.models.chat_message import ChatMessage
from fastapi import APIRouter, Response, status
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from backend_app.core.websocket import WSbroadcast
from backend_app.models.users import UserModel
from backend_app.models.visit import VisitModel
from shared.database import AsyncSessionDep

router = APIRouter()
REFRESH_DELTA_SECONDS    = 3
VISITOR_LIST_RANGE_DAY   = 90

stats_cache = {}
async def get_cache(name, calc_function, session: AsyncSessionDep, force_update = False):
    if name in stats_cache and not force_update:
        return stats_cache.get(name)
    stats_cache[name] = await calc_function(session)
    return stats_cache[name]

tft_stats = {}
def update_graphql_tft_stats():
    try:
        url = "https://api.teamfight.lol/graphql"
        query = """
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

        variables = {}
        response = requests.post(
            url,
            json={
                "operationName": "GetPlatformStats",
                "query": query,
                "variables": variables
            }
        )

        response.raise_for_status()
        stats = response.json()
        if not "getPlatformStats" in stats.get("data", {}):
            raise requests.HTTPError()
        tft_stats["total_games"] = stats["data"]["getPlatformStats"]["totalMatches"]
        tft_stats["gold_wasted"] = stats["data"]["getPlatformStats"].get("milestones", {}).get("goldWasted", 0)
    except requests.HTTPError:
        print("GRAPHQL STATS: Could not aquire stats for game")



async def created_accounts(session: AsyncSessionDep):
    total = int(await session.scalar(select(func.count()).select_from(UserModel))) or 0
    return {'count': total}

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
async def stats_dispatcher(name: str, response: Response, session: AsyncSessionDep):
    if name in endpoints:
        force_update = time.time() - endpoints[name].get("last", 0) > REFRESH_DELTA_SECONDS
        if endpoints[name].get("cache", False) is True:
            result = await get_cache(name, endpoints[name].get("function", default), session, force_update) or {}
        else:
            result = await endpoints[name].get("function", default)(session) or {}
        if force_update:
            endpoints[name]["last"] = time.time()
        # broadcast realtime stats to all users
        await WSbroadcast("stats.update", result)
        return result
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'success': False}
