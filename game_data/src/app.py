#!/usr/bin/env python3

import asyncio
import sys

import requests
from sqlalchemy.ext.asyncio import AsyncSession

from .classes import ChampionSummaryItem, DetailedChampion
from .fetch_matches.load_in_db import load_units_in_db
from .shared.database import db
from .shared.models.champions import Champion, champion_from_payload


async def main(
        session: AsyncSession
) -> None:
    print("\033[35mLoading Latest Champion Data\033[0m")
    
    champion_summary_json = requests.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json").json()
    champion_summary = [ChampionSummaryItem.model_validate(item) for item in champion_summary_json]
    
    for champion in champion_summary:
        detailed_champion_detail = DetailedChampion.model_validate(
            requests.get(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champion.id}.json").json()
        )

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
        print(f"\033[31mERROR\033[0m: {e.args[0] if e.args else e.with_traceback(None)}", file=sys.stderr)
        sys.exit(1)
