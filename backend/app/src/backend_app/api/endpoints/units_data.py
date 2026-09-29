import asyncio
import aiofiles
import json
from typing import Any

from fastapi import APIRouter, HTTPException, status
from httpx2 import AsyncClient, HTTPError
from pydantic import TypeAdapter

from backend_app.schemas.unit import Unit
from backend_app.core.dependencies import RedisDep 
import redis.exceptions as redis

router = APIRouter()

#ADAPT THAT TO SERVICES/ROUTES

units_adapter = TypeAdapter(list[Unit])
QUEUES = {"1100", "1160"}
RANKS = {"BRONZE", "CHALLENGER", "DIAMOND", "EMERALD", "GOLD", "GRANDMASTER", "IRON", "MASTER", "PLATINUM", "RANKUNKNOWN", "SILVER"}
SERVERS= {"BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "ME1", "NA1", "OC1", "RU", "SG2", "TR1", "TW2", "VN2"}

@router.get(
        "/units_data",
        response_model=list[Unit])
async def get_units_data(
    queue: str,
    rank: str,
    server: str,
    r: RedisDep
) -> list[Unit]:
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

    key = f"metatft:units:{queue}:{ranks_str}:{servers_str}"

    try:
        cached  = await r.get(key)
    except redis.RedisError:
        cached = None
    
    if cached is not None:
        return units_adapter.validate_json(cached)

    async with AsyncClient(timeout=10) as client:
        try:
            units, set_data = await asyncio.gather(
                fetch_units(client, queue, ranks_str, servers_str),
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

    if units is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Units data not found"
        )

    champions_by_id = {c["apiName"]: c for c in set_data["champions"]}
    units = [unit for unit in units if "TFT" not in unit["unit"]]
    units = [unit for unit in units if unit["unit"] in champions_by_id]

    all_units_use = get_all_units_use(units)

    try:
        async with aiofiles.open("app/src/shared/models_3d/models_list.json", 'r') as f:
            model_dict = json.loads(await f.read())
    except FileNotFoundError:
        model_dict = {}

    units_out = [
        process_unit(unit, all_units_use, champions_by_id, model_dict)
        for unit in units
    ]

    try:
        await r.set(key, units_adapter.dump_json(units_out), ex=900)
    except redis.RedisError :
        pass

    return units_out


def get_model(
    id: str,
    model_dict: dict[str, str]
) -> str:
    if model_dict:
        if id in model_dict:
            return model_dict[id]

    return ""


def process_unit(
    unit: dict[str, Any],
    all_units_use: int,
    champions_by_id: dict[str, dict[str, Any]],
    model_dict: dict[str, str]
) -> Unit:

    id = unit["unit"]
    places = unit["places"]

    total_unit_use = sum(places)
    avg_place = get_avg_place(places, total_unit_use)
    winrate = get_winrate(places, total_unit_use)
    frequency = get_frequency(total_unit_use, all_units_use)

    champion_info = champions_by_id[id]

    name = champion_info["name"]
    cost = champion_info["cost"]
    traits = [trait for trait in champion_info["traits"]]

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=128,height=128,format=auto/https://cdn.metatft.com/file/metatft/champions/tft18_" + name.lower() + ".png"
    model = model_dict.get(id)

    return (Unit(
        id=id,
        name=name,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        cost=cost,
        traits=traits,
        icon=icon,
        model=model,
    ))


def get_all_units_use(
        units: list
) -> int:
    total = 0

    for unit in units:
        total += sum(unit["places"])

    return (total)


def get_avg_place(
        places: list,
        total_unit_use: int
) -> float:
    weighted = 0

    for rank, count in enumerate(places, start=1):
        weighted += rank * count

    weighted /= total_unit_use

    return (weighted)


def get_winrate(
        places: list,
        total_unit_use: int
) -> float:
    winrate = (places[0] / total_unit_use) * 100

    return (winrate)


def get_frequency(
        total_unit_use: int,
        all_units_use: int
) -> float:
    if all_units_use == 0:
        return 0

    frequency = (total_unit_use / all_units_use) * 100

    return (frequency)


async def fetch_units(
    client: AsyncClient,
    queue: str,
    ranks: str,
    servers: str,
) -> list[dict[str, Any]]:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/units?queue={queue}&rank={ranks}&server={servers}")
    resp.raise_for_status()

    return resp.json()["results"]


async def fetch_set_data(
    client: AsyncClient
) -> list[dict[str, Any]]:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next((entry for entry in resp.json()["setData"] if entry["mutator"] == "TFTSet18"), None)