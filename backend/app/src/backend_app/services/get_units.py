import asyncio
import json
from typing import Any

import aiofiles
import redis.asyncio as redis
from httpx2 import AsyncClient, HTTPError
from pydantic import TypeAdapter

from backend_app.schemas.trait import Trait
from backend_app.schemas.unit import Unit
from backend_app.schemas.unit_trait import UnitTrait
from backend_app.services.fetch_game_data import (
    fetch_results,
    fetch_set_data,
    get_game_data,
)
from backend_app.services.get_stats import get_all_datas_use, get_stats


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
                fetch_results(client, "units", queue, ranks, servers),
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
        async with aiofiles.open("/app/src/shared/models_3d/models_list.json", 'r') as f:
            model_dict = json.loads(await f.read())
    except FileNotFoundError:
        model_dict = {}
        print("[get_units] model_list.json not found")

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

    names_to_mod = ["Master Yi", "Mama Beak", "Elder Dragon"]
    if name in names_to_mod:
        name = name.replace(" ", "")

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=128,height=128,format=auto/https://cdn.metatft.com/file/metatft/champions/tft18_" + name.lower().replace("'", "") + ".png"
    model = f"models_3d/{model_dict.get(id)}"

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