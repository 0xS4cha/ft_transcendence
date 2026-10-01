from fastapi import APIRouter, HTTPException, status

from backend_app.schemas.trait import Trait
from backend_app.core.dependencies import RedisDep 
from backend_app.core.cache import build_cache_key, get_or_fetch
from backend_app.services.get_traits import get_traits, TraitsUnavailableError, traits_adapter

router = APIRouter()

QUEUES = {"1100", "1160"}
RANKS = {"BRONZE", "CHALLENGER", "DIAMOND", "EMERALD", "GOLD", "GRANDMASTER", "IRON", "MASTER", "PLATINUM", "RANKUNKNOWN", "SILVER"}
SERVERS= {"BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "ME1", "NA1", "OC1", "RU", "SG2", "TR1", "TW2", "VN2"}

@router.get(
        "/traits_data",
        response_model=list[Trait])
async def get_traits_data(
    queue: str,
    rank: str,
    server: str,
    r: RedisDep
) -> list[Trait]:
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

    key = build_cache_key("traits", queue, ranks_str, servers_str)

    try:
        traits = await get_or_fetch(r, key, traits_adapter, lambda: get_traits(r, queue, ranks_str, servers_str))
    except TraitsUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        ) from e

    return traits