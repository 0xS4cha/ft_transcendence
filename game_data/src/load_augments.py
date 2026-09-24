import asyncio
import json
import sys
from typing import Any

from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models.augments import Augment


def create_augment(
        id: str,
        name: str,
        rarity: str,
        rounds: list[str],
        icon: str,
) -> Augment:
    augment = Augment(
        id=id,
        name=name,
        rarity=rarity,
        rounds=rounds,
        icon=icon,
    )

    return augment


async def add_augment(
    session: AsyncSession,
    augment: dict[str, Any]
) -> None:
    id = augment["apiName"]
    name = augment["name"]
    rarity = augment["rarity"]
    rounds = augment["rounds"]
    icon = f"https://cdn.metatft.com/file/metatft/augments/{augment["icon"].lower()}.png"

    existing = await session.get(Augment, id)
    if existing is not None:
        await session.delete(existing)
        await session.flush()

    session.add(create_augment(
        id,
        name,
        rarity,
        rounds,
        icon)
    )

    print(f"Saved augment \033[35m{name}\033[0m")


async def main(
    session: AsyncSession
) -> None:
    async with AsyncClient(timeout=10) as client:
        resp = await client.get("https://data.metatft.com/lookups/TFTSet18_latest_en_us.json")
        resp.raise_for_status()
        augments = resp.json()["augments"]

    for augment in augments:
        await add_augment(session, augment)
        
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
