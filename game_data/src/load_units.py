import asyncio
import json
import sys

import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models.units import Unit


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

def create_unit(
        id: str,
        avg_place: float,
        winrate: float,
        frequency: float,
        name: str,
        icon: str
) -> Unit:
    unit = Unit(
        id=id,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        name=name,
        icon=icon
    )
    return unit

def get_name(
    name: str
) -> str:

    to_replace = ["DA", "18", "_", "AP", "AD", "Small"]
    replaced = name
    for word in to_replace:
        replaced = replaced.replace(word, "")

    if replaced == "CrimsonRaptor":
        replaced = "MamaBeak"

    if replaced == "Sentry":
            replaced = "Pebbles"
    
    return replaced




async def main(
        session: AsyncSession
) -> None:
    units_data = {}
    async with aiofiles.open("/opt/game_data/units.json", 'r') as f:
        units_data = json.loads(await f.read())

    units = units_data["results"]
    all_units_use = get_all_units_use(units)

    for unit in units:
        if (unit["unit"].find("TFT") != -1):
            continue
        id = unit["unit"]
        places = unit["places"]
        total_unit_use = sum(places)
        avg_place = get_avg_place(places, total_unit_use)
        winrate = get_winrate(places, total_unit_use)
        frequency = get_frequency(total_unit_use, all_units_use)
        name = get_name(id)
        icon = "https://cdn.metatft.com/cdn-cgi/image/width=64,height=64,format=auto/https://cdn.metatft.com/file/metatft/champions/tft18_" + name.lower() + ".png"

        existing = await session.get(Unit, id)
        if existing is not None:
            await session.delete(existing)
            await session.flush()
        
        session.add(create_unit(id, avg_place, winrate, frequency, name, icon))

        print(f"Saved unit \033[35m{name}\033[0m")
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