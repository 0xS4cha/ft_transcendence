import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, status
from httpx2 import AsyncClient, HTTPError
from pydantic import TypeAdapter

from backend_app.schemas.trait import Trait
from backend_app.core.dependencies import RedisDep 
import redis.exceptions as redis

router = APIRouter()

#ADAPT THAT TO SERVICES/ROUTES

traits_adapter = TypeAdapter(list[Trait])
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

    key = f"metatft:traits:{queue}:{ranks_str}:{servers_str}"

    try:
        cached  = await r.get(key)
    except redis.RedisError:
        cached = None
    
    if cached is not None:
        return traits_adapter.validate_json(cached)

    async with AsyncClient(timeout=10) as client:
        try:
            traits, set_data = await asyncio.gather(
                fetch_traits(client, queue, ranks_str, servers_str),
                fetch_set_data(client)
            )
        except HTTPError as e:
            raise HTTPException(
                status_code = status.HTTP_502_BAD_GATEWAY,
                detail="Upstream Error"
            ) from e

    if set_data is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Set data not found"
        )

    if traits is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Traits data not found"
        )

    traits_by_id = {c["apiName"]: c for c in set_data["traits"]}
    traits = [trait for trait in traits if trait["trait"][:-2] in traits_by_id]

    all_traits_use = get_all_traits_use(traits)

    traits_out = [
        process_trait(trait, all_traits_use, traits_by_id)
        for trait in traits
    ]

    try:
        await r.set(key, traits_adapter.dump_json(traits_out), ex=900)
    except redis.RedisError :
        pass

    return traits_out


def get_model(
    id: str,
    model_dict: dict[str, str]
) -> str:
    if model_dict:
        if id in model_dict:
            return model_dict[id]

    return ""


def process_trait(
    trait: dict[str, Any],
    all_traits_use: int,
    traits_by_id: dict[str, dict[str, Any]]
) -> Trait:

    id = trait["trait"]
    places = trait["places"]

    total_trait_use = sum(places)
    avg_place = get_avg_place(places, total_trait_use)
    winrate = get_winrate(places, total_trait_use)
    frequency = get_frequency(total_trait_use, all_traits_use)

    trait_info = traits_by_id[id[:-2]]

    name = trait_info["name"]
    
    breakpoints = get_breakpoints(trait_info)
    breakpoint = breakpoints[int(id[-1]) - 1]

    icon = "https://cdn.metatft.com/file/metatft/traits/" + id[:-2].lower() + ".png"
    background_icon = get_background_icon(id, name, breakpoint)

    return (Trait(
        id=id,
        name=name,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        breakpoint=breakpoint,
        breakpoints=breakpoints,
        icon=icon,
        background_icon=background_icon,
    ))


async def fetch_traits(
    client: AsyncClient,
    queue: str,
    ranks: str,
    servers: str,
) -> list[dict[str, Any]]:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/traits?queue={queue}&rank={ranks}&server={servers}")
    resp.raise_for_status()

    return resp.json()["results"]


async def fetch_set_data(
    client: AsyncClient
) -> dict[str, Any] | None:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next((entry for entry in resp.json()["setData"] if entry["mutator"] == "TFTSet18"), None)

## CHNAGE TO 
class Switch:
    def __init__(self):
        self.unique = "https://cdn.metatft.com/file/metatft/traits/unique.png"
        self.plat = "https://cdn.metatft.com/file/metatft/traits/plat.png"
        self.gold = "https://cdn.metatft.com/file/metatft/traits/gold.png"
        self.silver = "https://cdn.metatft.com/file/metatft/traits/silver.png"
        self.bronze = "https://cdn.metatft.com/file/metatft/traits/bronze.png"
        self.none = "None"

    def case_0(self, id, name):
        return self.unique

    def case_1(self, id, name):
        if "Flora" in name:
            return self.bronze
        elif "Rival" in name:
            if id[-1] == "2":
                return self.bronze
            return self.gold
        else:
            return self.unique

    def case_2(self, id, name):
        if "Flora" in name or "Rival" in name:
            return self.gold
        else:
            return self.bronze

    def case_3(self, id, name):
        if "Summoner" in name or "Solar" in name:
            return self.gold
        elif "Riftbeast" in name \
            or "Edlerwood" in name \
            or "Sprykin" in name \
            or "Blossom" in name \
            or "Coven" in name:
            return self.bronze
        else:
            return self.silver

    def case_4(self, id, name):
        if "Executioner" in name \
            or "Primal" in name \
            or "Adaptor" in name \
            or "Fae" in name:
            return self.gold
        else:
            return self.silver

    def case_5(self, id, name):
        if "Riftbeast" in name \
            or "Edlerwood" in name \
            or "Sprykin" in name \
            or "Blossom" in name \
            or "Coven" in name:
            return self.silver
        else:
            return self.gold

    def case_6(self, id, name):
        return self.gold

    def case_7(self, id, name):
        return self.gold

    def case_9(self, id, name):
        return self.gold

    def case_10(self, id, name):
        return self.gold

    def case_11(self, id, name):
        return self.gold

    def default(self):
        return self.none

    def switch(self, value, id, name):
        return getattr(self, f"case_{value}", self.default)(id, name)
    

def get_all_traits_use(
        traits: list
) -> int:
    total = 0

    for trait in traits:
        total += sum(trait["places"])

    return (total)


def get_avg_place(
        places: list,
        total_trait_use: int
) -> float:
    weighted = 0

    for rank, count in enumerate(places, start=1):
        weighted += rank * count

    weighted /= total_trait_use

    return (weighted)


def get_winrate(
        places: list,
        total_trait_use: int
) -> float:
    winrate = (places[0] / total_trait_use) * 100

    return (winrate)


def get_frequency(
        total_trait_use: int,
        all_traits_use: int
) -> float:
    if all_traits_use == 0:
        return 0

    frequency = (total_trait_use / all_traits_use) * 100

    return (frequency)


def get_breakpoints(
    unit_trait_info: dict[str, Any]
) -> list[str]:
    effects = unit_trait_info["effects"]

    breakpoints = []
    for breakpoint in effects:
        if str(breakpoint["minUnits"]) == "None":
            breakpoints.append("0")
        else:
            breakpoints.append(str(breakpoint["minUnits"]))

    return breakpoints


def get_background_icon(
    id: str,
    name: str,
    breakpoint: str
) -> str:
    obj = Switch()
    return (obj.switch(breakpoint, id, name))