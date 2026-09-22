#!/usr/bin/env python3

import asyncio
import sys

from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .classes import ChampionSummaryItem, DetailedChampion
from .fetch_matches.load_in_db import load_units_in_db
from .shared.database import db
from .shared.models.champions import Champion, champion_from_payload


async def fetch_champions(
        client: AsyncClient,
        champion_id: int,
        sem: asyncio.Semaphore
) -> DetailedChampion:
    # async get a champion and return a valid DetailedChampion model
    async with sem:
        resp = await client.get(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champion_id}.json")
        resp.raise_for_status()
        return DetailedChampion.model_validate(resp.json())


async def main(
        session: AsyncSession
) -> None:
    print("\033[35mLoading Latest Champion Data\033[0m")

    # 15 requests at a time
    sem = asyncio.Semaphore(15)

    # get champion list
    # use their id to fetch the details on each champion
    async with AsyncClient(timeout=10) as client:
        resp = await client.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json")
        champion_summary = [ChampionSummaryItem.model_validate(item) for item in resp.json()]

        # creates a list of c tasks, then asyncio runs them asynchronously
        details = await asyncio.gather(
            *(fetch_champions(client, c.id, sem)
              for c in champion_summary)
        )

    # if champion already exists, delete and add fresh one, if not just add 
    for detailed_champion_detail in details:
        existing = await session.get(Champion, detailed_champion_detail.id)
        if existing is not None:
            await session.delete(existing)
            await session.flush()
        session.add(champion_from_payload(detailed_champion_detail))

        print(f"Saved champion \033[35m{detailed_champion_detail.name}\033[0m")
    await session.commit()
        
    # try to load computed matches stats into memory
    try:
        await load_units_in_db(session)
    except Exception as e:  # noqa: BLE001
        print(f"Could not load computed games in database: {e}")
        sys.exit(1)


async def run():
    async with db.async_session_factory() as session:
        await main(session)

      
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:  # noqa: BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)
