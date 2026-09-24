import asyncio
import json
import sys
from typing import Any

import aiofiles
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models.traits import Trait


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


def create_trait(
        id: str,
        avg_place: float,
        winrate: float,
        frequency: float,
        name: str,
        breakpoint: str,
        breakpoints: list[str],
        icon: str,
        background_icon: str
) -> Trait:
    trait = Trait(
        id=id,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        name=name,
        breakpoint=breakpoint,
        breakpoints=breakpoints,
        icon=icon,
        background_icon=background_icon,
    )

    return trait


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


async def add_trait(
    session: AsyncSession,
    trait: dict[str, Any],
    all_traits_use: int,
    trait_info: list[dict[str, Any]]
) -> None:
    id = trait["trait"]
    places = trait["places"]

    total_trait_use = sum(places)
    avg_place = get_avg_place(places, total_trait_use)
    winrate = get_winrate(places, total_trait_use)
    frequency = get_frequency(total_trait_use, all_traits_use)

    unit_trait_info = next(entry for entry in trait_info if entry["apiName"] == id[:-2])
    name = unit_trait_info["name"]

    breakpoints = get_breakpoints(unit_trait_info)
    breakpoint = breakpoints[int(id[-1]) - 1]

    icon = "https://cdn.metatft.com/file/metatft/traits/" + id[:-2].lower() + ".png"
    background_icon = get_background_icon(id, name, breakpoint)

    existing = await session.get(Trait, id)
    if existing is not None:
        await session.delete(existing)
        await session.flush()
    
    session.add(create_trait(
        id,
        avg_place,
        winrate,
        frequency,
        name,
        breakpoint,
        breakpoints,
        icon,
        background_icon)
    )

    print(f"Saved trait \033[35m{name}\033[0m")


async def main(
    session: AsyncSession
) -> None:
    trait_data = {}
    async with aiofiles.open("/opt/game_data/traits.json", 'r') as f:
        trait_data = json.loads(await f.read())

    async with AsyncClient(timeout=10) as client:
        resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
        resp.raise_for_status()
        trait_info = next(entry for entry in resp.json()["setData"] if entry["mutator"] == "TFTSet18")["traits"]

    traits = trait_data["results"]
    all_traits_use = get_all_traits_use(traits)

    for trait in traits:
        await add_trait(session, trait, all_traits_use, trait_info)
        
    await session.commit()


async def run():
    async with db.async_session_factory() as session:
        await main(session)


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e: #noqa BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)
