import asyncio
from typing import Any

from fastapi import APIRouter
from httpx2 import AsyncClient

from backend.app.src.backend_app.schemas.unit import Unit

router = APIRouter()

# @router.get("/units_data")
# async def get_units_data(
#     session: AsyncSessionDep
# ) -> list[dict[str, Any]]:
#     units = (await session.scalars(select(Unit))).all()
#     to_serialize = [model_to_dict(unit) for unit in units]
    
#     return to_serialize

@router.get(
        "/units_data?queue={queue}?rank={rank_list}?server={server_list}",
        response_model=list[Unit])
async def get_units_data(
    queue: str,
    rank_list: list[str],
    server_list: list[str],
) -> list[Unit]:

    #filter whitelist
    #lookup cache

    async with AsyncClient(timeout=10) as client:
        units, champions_info = asyncio.gather(
            fetch_units(client),
            fetch_champions_info(client)
        )

    all_units_use = get_all_units_use(units)
    for unit in units:
        add_unit(unit, all_units_use, champions_info)

    
def add_unit(
    unit: dict[str, Any],
    all_units_use: int,
    champions_info: list[dict[str, Any]] 
) -> None:
    if (unit["unit"].find("TFT") != -1):
        return
    id = unit["unit"]
    places = unit["places"]

    total_unit_use = sum(places)
    avg_place = get_avg_place(places, total_unit_use)
    winrate = get_winrate(places, total_unit_use)
    frequency = get_frequency(total_unit_use, all_units_use)

    champion_info = next(entry for entry in champions_info if entry["apiName"] == id)
    name = champion_info["name"]
    cost = champion_info["cost"]
    traits = [trait for trait in champion_info["traits"]]

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=128,height=128,format=auto/https://cdn.metatft.com/file/metatft/champions/tft18_" + name.lower() + ".png"

    return (Unit(
        id=id,
        name=name,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        cost=cost,
        traits=traits,
        icon=icon,
        model="model"
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
    rank_list: list[str],
    server_list: list[str],
) -> list[dict[str, Any]]:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/units?queue={queue}?rank={rank_list}?server={server_list}")
    resp.raise_for_status()

    return resp.json()["results"]


async def fetch_champions_info(
    client: AsyncClient
) -> list[dict[str, Any]]:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next(entry for entry in resp.json()["setData"] if entry["mutator"] == "TFTSet18")["champions"]