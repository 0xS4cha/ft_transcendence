import asyncio
import json
import sys
from typing import Any

import aiofiles
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models.items import Item


def get_all_items_use(
        items: list
) -> int:
    total = 0

    for item in items:
        total += sum(item["places"])

    return (total)


def get_avg_place(
        places: list,
        total_item_use: int
) -> float:
    weighted = 0

    for rank, count in enumerate(places, start=1):
        weighted += rank * count

    weighted /= total_item_use

    return (weighted)


def get_winrate(
        places: list,
        total_item_use: int
) -> float:
    winrate = (places[0] / total_item_use) * 100

    return (winrate)


def get_frequency(
        total_item_use: int,
        all_items_use: int
) -> float:
    if all_items_use == 0:
        return 0

    frequency = (total_item_use / all_items_use) * 100

    return (frequency)


def create_item(
        id: str,
        avg_place: float,
        winrate: float,
        frequency: float,
        name: str,
        type: str,
        composition: list[str],
        icon: str
) -> Item:
    item = Item(
        id=id,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        name=name,
        type=type,
        composition=composition,
        icon=icon
    )
    return item


def get_type(
        name: str
) -> str:
    type = "Normal"
    to_find = ["Emblem", "Radiant", "Artifact", "Component"]

    for word in to_find:
        if name.find(word) != -1:
            type = word

    if name.find("Tactician") != -1:
        type += "-Component"
    return type


async def add_item(
    session: AsyncSession,
    item: dict[str, Any],
    all_items_use: int,
    items_compo: dict[str, Any]
) -> None:
    id = item["itemName"]
    places = item["places"]

    total_item_use = sum(places)
    avg_place = get_avg_place(places, total_item_use)
    winrate = get_winrate(places, total_item_use)
    frequency = get_frequency(total_item_use, all_items_use)

    name = next(entry["name"] for entry in items_compo if entry["apiName"] == id)
    type = get_type(id)
    composition = next(entry["composition"] for entry in items_compo if entry["apiName"] == id)

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=64,height=64,format=auto/https://cdn.metatft.com/file/metatft/items/" + id.lower() + ".png"

    existing = await session.get(Item, id)
    if existing is not None:
        await session.delete(existing)
        await session.flush()
    
    session.add(create_item(
        id,
        avg_place,
        winrate,
        frequency, 
        name,
        type,
        composition,
        icon)
    )

    print(f"Saved item \033[35m{name}\033[0m")


async def main(
        session: AsyncSession
) -> None:
    item_data = {}
    async with aiofiles.open("/opt/game_data/items_matches.json", 'r') as f:
        item_data = json.loads(await f.read())

    async with AsyncClient(timeout=10) as client:
        resp = await client.get("https://data.metatft.com/lookups/TFTSet18_latest_en_us.json")
        resp.raise_for_status()
        items_compo = resp.json()["items"]

    items = item_data["results"]
    all_items_use = get_all_items_use(items)

    for item in items:
        await add_item(session, item, all_items_use, items_compo)
        
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