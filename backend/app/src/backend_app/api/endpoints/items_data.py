from fastapi import APIRouter, HTTPException, status

from backend_app.schemas.item import Item
from backend_app.core.dependencies import RedisDep 
from backend_app.services.fetch_game_data import build_cache_key, get_or_fetch
from backend_app.services.get_items import get_items, ItemsUnavailableError, items_adapter

router = APIRouter()

QUEUES = {"1100", "1160"}
RANKS = {"BRONZE", "CHALLENGER", "DIAMOND", "EMERALD", "GOLD", "GRANDMASTER", "IRON", "MASTER", "PLATINUM", "RANKUNKNOWN", "SILVER"}
SERVERS= {"BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "ME1", "NA1", "OC1", "RU", "SG2", "TR1", "TW2", "VN2"}

@router.get(
        "/items_data",
        response_model=list[Item])
async def get_items_data(
    queue: str,
    rank: str,
    server: str,
    r: RedisDep
) -> list[Item]:
    ranks = sorted(rank.split(","))
    servers = sorted(server.split(","))
    
    if (
        queue not in QUEUES
        or any(rk not in RANKS for rk in ranks)
        or any(sv not in SERVERS for sv in servers)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filter")

    ranks_str = ",".join(ranks)
    servers_str = ",".join(servers)

    key = build_cache_key("items", queue, ranks_str, servers_str)

    try:
        items = await get_or_fetch(r, key, items_adapter, lambda: get_items(r, queue, ranks_str, servers_str))
    except ItemsUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        ) from e

    return items