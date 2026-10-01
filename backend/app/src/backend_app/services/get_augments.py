from typing import Any

from httpx2 import AsyncClient, HTTPError
from backend_app.schemas.augment import Augment
from pydantic import TypeAdapter
from backend_app.services.fetch_game_data import get_game_data, fetch_lookup
import redis.asyncio as redis

class AugmentsUnavailableError(Exception):
    pass

augments_adapter = TypeAdapter(list[Augment])

async def get_augments(
    r: redis.Redis
) -> list[Augment]:
    async with AsyncClient(timeout=10) as client:
        try:
            lookup = await get_game_data(r, "lookup", lambda: fetch_lookup(client))
        except HTTPError as e:
            raise AugmentsUnavailableError("Upstream Error") from e

    if lookup is None:
        raise AugmentsUnavailableError("Lookup data not found")

    augments =lookup.get("augments")

    if augments is None:
        raise AugmentsUnavailableError("Augments data not found")

    augments_out = [
        a for augment in augments
        if (a := process_augment(augment)) is not None
    ]

    return augments_out


def process_augment(
    augment: dict[str, Any]
) -> Augment | None:
    id = augment.get("apiName")
    name = augment.get("name")
    rarity = augment.get("rarity")
    rounds = augment.get("rounds")
    icon_path = augment.get("icon")

    if id is None or \
       name is None or \
       rarity is None or \
       rounds is None or \
       icon_path is None:
        return None

    icon = f"https://cdn.metatft.com/file/metatft/augments/{icon_path.lower()}.png"

    return (Augment(
        id=id,
        name=name,
        rarity=rarity,
        rounds=rounds,
        icon=icon
    ))