import asyncio
import aiofiles
import json
from typing import Any

from fastapi import APIRouter, HTTPException, status
from httpx2 import AsyncClient
from pydantic import TypeAdapter

from backend_app.schemas.unit import Unit
from backend_app.core.dependencies import RedisDep 

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
        raise HTTPException(status_code=400, detail="Invalid filter")

    ranks_str = ",".join(ranks)
    servers_str = ",".join(servers)

    key = f"metatft:units:{queue}:{ranks_str}:{servers_str}"
    
    cached  = await r.get(key)
    if cached is not None:
        return units_adapter.validate_json(cached)


    async with AsyncClient(timeout=10) as client:
        units, set_data = await asyncio.gather(
            fetch_units(client, queue, ranks_str, servers_str),
            fetch_set_data(client)
        )

    if set_data is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Set data not found"
        )

    champions_by_id = {
        c["apiName"]: c
        for c in set_data["champions"]
    }

    all_units_use = get_all_units_use(units)

    async with aiofiles.open("app/src/shared/models_3d/models_list.json", 'r') as f:
        model_dict = json.loads(await f.read())

    units_out = [
        u for raw in units
        if (u := process_unit(raw, all_units_use, champions_by_id, model_dict)) is not None
    ]

    await r.set(key, units_adapter.dump_json(units_out), ex=900)

    return units_out


#handle model name parsing
def parse_names(
    names: list[str]
) -> list[str]:
    names_lower = [name.lower() for name in names]
    
    to_change = ["gromp", "raptor", "kogmaw", "nidalee"]

    for index, name in enumerate(names_lower):
        for word in to_change:
            if word in name:
                names_lower[index] = f"da_18_{word}"
        if "small" in name:
            names_lower[index] = name.replace("small", "")

    return names_lower

def get_model(
    id: str,
    model_dict: dict[str, str]
) -> str:
    if id in model_dict:
        return model_dict[id]

    return ""


def process_unit(
    unit: dict[str, Any],
    all_units_use: int,
    champions_by_id: dict[str, dict[str, Any]],
    model_dict: dict[str, str]
) -> Unit | None:
    if (unit["unit"].find("TFT") != -1):
        return None
    id = unit["unit"]
    places = unit["places"]

    total_unit_use = sum(places)
    avg_place = get_avg_place(places, total_unit_use)
    winrate = get_winrate(places, total_unit_use)
    frequency = get_frequency(total_unit_use, all_units_use)

    if id in champions_by_id:
        champion_info = champions_by_id[id]
    else:
        return None
    
    name = champion_info["name"]
    cost = champion_info["cost"]
    traits = [trait for trait in champion_info["traits"]]

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=128,height=128,format=auto/https://cdn.metatft.com/file/metatft/champions/tft18_" + name.lower() + ".png"
    model = get_model(id, model_dict)

    return (Unit(
        id=id,
        name=name,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        cost=cost,
        traits=traits,
        icon=icon,
        model=model
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
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/units?queue={queue}?rank={ranks}?server={servers}")
    resp.raise_for_status()

    return resp.json()["results"]


async def fetch_set_data(
    client: AsyncClient
) -> list[dict[str, Any]]:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next((entry for entry in resp.json()["setData"] if entry["mutator"] == "TFTSet18"), None)