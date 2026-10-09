from typing import Any

import redis.asyncio as redis
from httpx2 import AsyncClient, HTTPError
from pydantic import TypeAdapter, ValidationError

from backend_app.schemas.augment import Augment
from backend_app.services.fetch_game_data import (
    dict_list,
    fetch_lookup,
    get_game_data,
)


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
        a for augment in dict_list(augments)
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
       not isinstance(icon_path, str):
        return None

    icon = f"https://cdn.metatft.com/file/metatft/augments/{icon_path.lower()}.png"

    try:
        return Augment(
            id=id,
            name=name,
            rarity=rarity,
            rounds=rounds,
            icon=icon
        )
    except ValidationError:
        return None