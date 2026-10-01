from typing import Any

from httpx2 import AsyncClient, HTTPError
from backend_app.schemas.augment import Augment
from pydantic import TypeAdapter
from backend_app.core.utils import safe_get

class AugmentsUnavailableError(Exception):
    pass

augments_adapter = TypeAdapter(list[Augment])

async def get_augments(
) -> list[Augment]:
    async with AsyncClient(timeout=10) as client:
        try:
            augments = fetch_augments(client)
        except HTTPError as e:
            raise AugmentsUnavailableError("Upstream Error") from e

    if augments is None:
        return AugmentsUnavailableError("Augments data not found")


    augments_out = [
        a for augment in augments
        if (a := process_augment(augment)) is not None
    ]

    return augments_out


async def process_augment(
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

    
async def fetch_augments(
    client: AsyncClient
) -> list[dict[str, Any]] | None:
    resp = await client.get("https://data.metatft.com/lookups/TFTSet18_latest_en_us.json")
    resp.raise_for_status()
    return resp.json().get("augments")