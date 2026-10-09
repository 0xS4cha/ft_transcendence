import asyncio
from typing import Any

import redis.asyncio as redis
from httpx2 import AsyncClient, HTTPError
from pydantic import TypeAdapter, ValidationError

from backend_app.core.utils import safe_get
from backend_app.schemas.trait import Trait
from backend_app.services.fetch_game_data import (
    dict_list,
    fetch_results,
    fetch_set_data,
    get_game_data,
)
from backend_app.services.get_stats import get_all_datas_use, get_stats, valid_places


class TraitsUnavailableError(Exception):
    pass

traits_adapter = TypeAdapter(list[Trait])

async def get_traits(
    r: redis.Redis,
    queue: str,
    ranks: str,
    servers: str
) -> list[Trait]:
    async with AsyncClient(timeout=10) as client:
        try:
            traits, set_data = await asyncio.gather(
                fetch_results(client, "traits", queue, ranks, servers),
                get_game_data(r, "set_data", lambda: fetch_set_data(client))
            )
        except HTTPError as e:
            raise TraitsUnavailableError("Upstream Error") from e

    if set_data is None:
        raise TraitsUnavailableError("Set data not found")

    if traits is None:
        raise TraitsUnavailableError("Traits data not found")

    traits_by_id = {
        c["apiName"]: c
        for c in dict_list(set_data.get("traits"))
        if isinstance(c.get("apiName"), str)
    }
    if not traits_by_id:
        raise TraitsUnavailableError("Set data traits api names not found")
    
    traits = [
        trait for trait in traits
        if isinstance(trait.get("trait"), str) and trait["trait"][:-2] in traits_by_id
    ]
    if not traits:
        raise TraitsUnavailableError("Traits not found in set data traits")

    all_traits_use = get_all_datas_use(traits)
    if all_traits_use == 0:
        raise TraitsUnavailableError("Traits use not found")

    traits_out = [
        t for trait in traits
        if (t := process_trait(trait, all_traits_use, traits_by_id)) is not None
    ]

    return traits_out


def process_trait(
    trait: dict[str, Any],
    all_traits_use: int,
    traits_by_id: dict[str, dict[str, Any]]
) -> Trait | None:

    id = trait.get("trait")
    places = valid_places(trait.get("places"))
    if not isinstance(id, str) or not id[-1:].isdigit() or places is None:
        return None

    total_trait_use = sum(places)
    if total_trait_use == 0:
        return None
    avg_place, winrate, frequency = get_stats(places, total_trait_use, all_traits_use)

    trait_info = traits_by_id.get(id[:-2])
    if trait_info is None:
        return None

    name = trait_info.get("name")
    if name is None:
        return None
    
    breakpoints = get_breakpoints(trait_info)
    if breakpoints is None:
        return None

    breakpoint = safe_get(breakpoints, int(id[-1]) - 1)
    if breakpoint is None:
        return None

    icon = "https://cdn.metatft.com/file/metatft/traits/" + id[:-2].lower() + ".png"
    background_icon = get_background_icon(id, name, breakpoint)
    if background_icon is None:
        return None

    try:
        return Trait(
            id=id,
            name=name,
            avg_place=avg_place,
            winrate=winrate,
            frequency=frequency,
            breakpoint=breakpoint,
            breakpoints=breakpoints,
            icon=icon,
            background_icon=background_icon,
        )
    except ValidationError:
        return None


def get_breakpoints(
    unit_trait_info: dict[str, Any]
) -> list[str] | None:
    effects = unit_trait_info.get("effects")
    if not isinstance(effects, list):
        return None

    breakpoints = []
    for breakpoint in effects:
        if not isinstance(breakpoint, dict) or "minUnits" not in breakpoint:
            return None
        elif breakpoint["minUnits"] is None:
            breakpoints.append("0")
        else:
            breakpoints.append(str(breakpoint["minUnits"]))

    return breakpoints


def get_background_icon(
    id: str,
    name: str,
    breakpoint: str
) -> str | None:
    unique = "https://cdn.metatft.com/file/metatft/traits/unique.png"
    plat = "https://cdn.metatft.com/file/metatft/traits/plat.png"
    gold = "https://cdn.metatft.com/file/metatft/traits/gold.png"
    silver = "https://cdn.metatft.com/file/metatft/traits/silver.png"
    bronze = "https://cdn.metatft.com/file/metatft/traits/bronze.png"

    match breakpoint:
        case "0":
            return unique
        
        case "1":
            if "Flora" in name:
                return bronze
            elif "Rival" in name:
                if id[-1] == "2":
                    return bronze
                return gold
            else:
                return unique

        case "2":
            if "Flora" in name or "Rival" in name:
                return gold
            else:
                return bronze

        case "3":
            if "Summoner" in name or "Solar" in name:
                return gold
            elif "Riftbeast" in name \
                or "Edlerwood" in name \
                or "Sprykin" in name \
                or "Blossom" in name \
                or "Coven" in name:
                return bronze
            else:
                return silver

        case "4":
            if "Executioner" in name \
                or "Primal" in name \
                or "Adaptor" in name \
                or "Fae" in name:
                return gold
            else:
                return silver

        case "5":
            if "Riftbeast" in name \
                or "Edlerwood" in name \
                or "Sprykin" in name \
                or "Blossom" in name \
                or "Coven" in name:
                return silver
            else:
                return gold

        case "6" | "7" | "8" | "9" | "10":
            return gold

        case "11":
            return plat

        case _:
            return None
