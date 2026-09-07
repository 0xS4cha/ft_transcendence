#!/usr/bin/env python3

import os

import requests
import sys
import time


from .classes import ChampionSummaryItem, DetailedChampion
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .shared.models import Base, Champion, champion_from_payload
from .fetch_matches.load_in_db import load_units_in_db


def main() -> None:
    print("\033[35mLoading Latest Champion Data\033[0m")
    db_url = os.environ['DATABASE_URL'].replace("postgres://", "postgresql+psycopg2://", 1)
    print(f"DATABASE_URL: \033[35m{db_url}\033[0m")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    champion_summary_json = requests.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json").json()
    champion_summary = [ChampionSummaryItem.model_validate(item) for item in champion_summary_json]
    with Session(engine) as session:
        for champion in champion_summary:
            detailed_champion_detail = DetailedChampion.model_validate(
                requests.get(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champion.id}.json").json()
            )

            existing = session.get(Champion, detailed_champion_detail.id)
            if existing is not None:
                session.delete(existing)
                session.flush()
            session.add(champion_from_payload(detailed_champion_detail))

            print(f"Saved champion \033[35m{detailed_champion_detail.name}\033[0m")
        session.commit()

    # try to load computed matches stats into memory
    try:
        load_units_in_db(engine)
    except Exception as e:
        print(f"Could not load computed games in database: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[31mERROR\033[0m: {e.args[0] if e.args else e.with_traceback(None)}", file=sys.stderr)
        sys.exit(1)
