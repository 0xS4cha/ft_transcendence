import asyncio
import aiofiles
import json
from typing import Any

from httpx2 import AsyncClient, HTTPError
from backend_app.schemas.unit import Unit
from backend_app.schemas.unit_trait import UnitTrait
from backend_app.schemas.trait import Trait
from pydantic import TypeAdapter
from backend_app.core.utils import safe_get
from backend_app.services.fetch_game_data import get_game_data, fetch_set_data
from backend_app.services.get_stats import get_all_datas_use, get_stats
import redis.asyncio as redis

class UnitsUnavailableError(Exception):
    pass

units_adapter = TypeAdapter(list[Unit])

async def get_units(
    r: redis.Redis,
    queue: str,
    ranks: str,
    servers: str,
    traits: list[Trait],
) -> list[Unit]:
    async with AsyncClient(timeout=10) as client:
        try:
            units, set_data = await asyncio.gather(
                fetch_units(client, queue, ranks, servers),
                get_game_data(r, "set_data", lambda: fetch_set_data(client))
            )
        except HTTPError as e:
            raise UnitsUnavailableError("Upstream Error") from e

    if set_data is None:
        raise UnitsUnavailableError("Set data not found")

    if units is None:
        raise UnitsUnavailableError("Trait data not found")

    champions_by_id = {
        c["apiName"]: c
        for c in set_data.get("champions", [])
        if "apiName" in c
    }
    if not champions_by_id:
        raise UnitsUnavailableError("Set data champions api names not found")

    units = [unit for unit in units if "TFT" not in unit.get("unit", "")]
    units = [unit for unit in units if unit.get("unit", "") in champions_by_id]
    if not units:
        raise UnitsUnavailableError("Units not found in set data units")

    all_units_use = get_all_datas_use(units)
    if all_units_use == 0:
        raise UnitsUnavailableError("Units use not found")

    try:
        async with aiofiles.open("app/src/shared/models_3d/models_list.json", 'r') as f:
            model_dict = json.loads(await f.read())
    except FileNotFoundError:
        model_dict = {}

    units_out = [
        process_unit(unit, all_units_use, champions_by_id, model_dict, traits)
        for unit in units
    ]

    return units_out


def process_unit(
    unit: dict[str, Any],
    all_units_use: int,
    champions_by_id: dict[str, dict[str, Any]],
    model_dict: dict[str, str],
    traits_list: list[Trait]
) -> Unit | None:

    id = unit.get("unit")
    places = unit.get("places")
    if id is None or places is None:
        return None

    total_unit_use = sum(places)
    if total_unit_use == 0:
        return None
    avg_place, winrate, frequency = get_stats(places, total_unit_use, all_units_use)

    champion_info = champions_by_id.get(id)
    if champion_info is None:
        return None

    name = champion_info.get("name")
    cost = champion_info.get("cost")
    if name is None or cost is None:
        return None
    
    traits = []
    seen_names = set()

    for trait_name in champion_info.get("traits", []):
        for trait in traits_list:
            if trait.name == trait_name and trait_name not in seen_names:
                traits.append(UnitTrait.model_validate(trait, from_attributes=True))
                seen_names.add(trait_name)
                break

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
        total += sum(unit.get("places"))

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
    winrate = (safe_get(places,0) / total_unit_use) * 100

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
) -> list[dict[str, Any]] | None:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/units?queue={queue}&rank={ranks}&server={servers}")
    resp.raise_for_status()

    return resp.json().get("results")