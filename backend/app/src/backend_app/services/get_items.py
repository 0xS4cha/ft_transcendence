import asyncio
from typing import Any

from httpx2 import AsyncClient, HTTPError
from backend_app.schemas.item import Item
from pydantic import TypeAdapter
from backend_app.core.utils import safe_get
from backend_app.services.fetch_game_data import get_game_data, fetch_lookup
import redis.asyncio as redis
from backend_app.services.get_stats import get_all_datas_use, get_stats

class ItemsUnavailableError(Exception):
    pass

items_adapter = TypeAdapter(list[Item])

async def get_items(
    r: redis.Redis,
    queue: str,
    ranks: str,
    servers: str
) -> list[Item]:
    async with AsyncClient(timeout=10) as client:
        try:
            items, lookup = await asyncio.gather(
                fetch_items(client, queue, ranks, servers),
                get_game_data(r, "lookup", lambda: fetch_lookup(client))
            )
        except HTTPError as e:
            raise ItemsUnavailableError("Upstream Error") from e

    if lookup is None:
        raise ItemsUnavailableError("Lookup data not found")

    items_compo = lookup.get("items") 

    if items_compo is None:
        raise ItemsUnavailableError("Set data not found")

    if items is None:
        raise ItemsUnavailableError("Items data not found")

    items_by_id = {
        c["apiName"]: c
        for c in items_compo
        if "apiName" in c
    }
    if not items_by_id:
        raise ItemsUnavailableError("Items compo api names not found")
    
    items = [item for item in items if item.get("itemName", "") in items_by_id]
    if not items:
        raise ItemsUnavailableError("Items not found in items compo")

    all_items_use = get_all_datas_use(items)
    if all_items_use == 0:
        raise ItemsUnavailableError("Items use not found")

    items_out = [
        t for item in items
        if (t := process_item(item, all_items_use, items_by_id)) is not None
    ]

    return items_out


def process_item(
    item: dict[str, Any],
    all_items_use: int,
    items_by_id: dict[str, dict[str, Any]]
) -> Item | None:

    id = item.get("itemName")
    places = item.get("places")
    if id is None or places is None:
        return None

    total_item_use = sum(places)
    if total_item_use == 0:
        return None
    avg_place, winrate, frequency = get_stats(places, total_item_use, all_items_use)

    item_info = items_by_id.get(id)
    if item_info is None:
        return None

    name = item_info.get("name")
    if name is None:
        return None

    type = get_type(id)
    composition = item_info.get("composition")
    if composition is None:
        return None

    icon = "https://cdn.metatft.com/cdn-cgi/image/width=128,height=128,format=auto/https://cdn.metatft.com/file/metatft/items/" + id.lower() + ".png"
    
    return (Item(
        id=id,
        name=name,
        avg_place=avg_place,
        winrate=winrate,
        frequency=frequency,
        type=type,
        composition=composition,
        icon=icon,
    ))


def get_type(
    name: str
) -> str:
    type = "Normal"
    to_find = ["Emblem", "Radiant", "Artifact", "Component"]

    for word in to_find:
        if word in name:
            type = word
    
    return type


async def fetch_items(
    client: AsyncClient,
    queue: str,
    ranks: str,
    servers: str,
) -> list[dict[str, Any]] | None:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/items_matches?queue={queue}&rank={ranks}&server={servers}")
    resp.raise_for_status()

    return resp.json().get("results")


def get_all_items_use(
        items: list
) -> int:
    total = 0

    for item in items:
        total += sum(item.get("places"), 0)

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
    winrate = (safe_get(places, 0) / total_item_use) * 100

    return (winrate)


def get_frequency(
        total_item_use: int,
        all_items_use: int
) -> float:
    if all_items_use == 0:
        return 0

    frequency = (total_item_use / all_items_use) * 100

    return (frequency)
