import asyncio
import json
import sys

import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models.items import Item

#item

#avg place (1*number of 1st place + ... + 8*number of 8th places) / number of places of 1st place + ... + number of 8th places
#wr number of 1st places compared to number of all places
#frequency number of all places compared to number of all places of all items

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
    frequency = (total_item_use / all_items_use) * 100

    return (frequency)

def create_item(
        id: str,
        avg_place: float,
        winrate: float,
        frequency: float,
        name: str
) -> Item:
    item = Item(
        id=id,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        name=name
    )
    return item

def get_name(
    name: str
) -> str:

    to_replace = ["DA", "18", "_", "Emblem", "Radiant", "Artifact", "Component"]
    replaced = name
    for word in to_replace:
        replaced = replaced.replace(word, "")

    name_list = [ch for ch in replaced]

    true_name_list = []
    for index, ch in enumerate(name_list):
        if ch.isupper():
            if index+1 < len(name_list) and name_list[index + 1].isupper():
                true_name_list.append(ch)
            else:
                true_name_list.append(" " + ch)
        else:
            true_name_list.append(ch)

    true_name = "".join(true_name_list).strip()
    
    return true_name

async def main(
        session: AsyncSession
) -> None:
    item_data = {}
    async with aiofiles.open("/opt/game_data/items.json", 'r') as f:
        item_data = json.loads(await f.read())

    items = item_data["results"]
    all_items_use = get_all_items_use(items)
    for item in items:
        id = item["itemName"]
        places = item["places"]
        total_item_use = sum(places)
        avg_place = get_avg_place(places, total_item_use)
        winrate = get_winrate(places, total_item_use)
        frequency = get_frequency(total_item_use, all_items_use)
        name = get_name(id)

        existing = await session.get(Item, id)
        if existing is not None:
            await session.delete(existing)
            await session.flush()
        session.add(create_item(id, avg_place, winrate, frequency, name))

        print(f"Saved item \033[35m{name}\033[0m")
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