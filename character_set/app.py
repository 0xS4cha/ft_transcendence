#!/usr/bin/env python3

import os

import requests
import json
import sys
import time


from classes import ChampionSummaryItem, DetailedChampion
from sqlalchemy import create_engine


def main() -> None:
    print("\033[35mLoading Latest Champion Data\033[0m")
    engine = create_engine(os.environ['DATABASE_URL'])
    
    champion_summary_json = requests.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json").json()
    champion_summary = [ChampionSummaryItem.model_validate(item) for item in champion_summary_json]
    for champion in champion_summary:
        detailed_champion_detail = DetailedChampion.model_validate(
            requests.get(f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/{champion.id}.json").json()
        )
        
        print(detailed_champion_detail)
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\033[31mERROR\033[0m: {e.args[0] if e.args else e.with_traceback(None)}", file=sys.stderr)
