import datetime
import json
import os
import random
import sys
import time
import requests


API_KEYS = [
    key.strip()
    for key in os.environ.get("RIOT_API_KEYS", "").split(";")
    if key.strip()
]
SERVER = "asia"
REGIONAL_HOST = f"https://{SERVER}.api.riotgames.com"
current_api_key = 0
API_RETRIES = 5

def riot_get(url, params=None):
    try:
        for retry_idx in range(API_RETRIES):
            response = None
            try:
                headers = {
                    "X-Riot-Token": API_KEYS[current_api_key].strip(),
                }

                response = requests.get(
                    f"{REGIONAL_HOST}{url}",
                    headers=headers,
                    params=params,
                    timeout=10,
                )
                if response.status_code != 200:
                    print(f"RIOT api failed: {response.status_code} {response.text} retrying: [{retry_idx}/{API_RETRIES}]")
                    raise ConnectionAbortedError()
                return response.json()
            except ConnectionAbortedError:
                print("Sleeping for 2min to reset rate limit...")
                time.sleep(120)
                pass
        raise Exception(f"Riot API error")
    except KeyboardInterrupt:
        raise Exception("Keyboard Interrupt")


def get_account(GAME_NAME, TAG_LINE):
    return riot_get(f"/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}")

def get_match_ids(puuid):
    return riot_get(
        f"/tft/match/v1/matches/by-puuid/{puuid}/ids",
        params={
            "start": 0,
            "count": 10,
        },
    )


def get_match(match_id):
    return riot_get(f"/tft/match/v1/matches/{match_id}")


def find_player(match, puuid):
    for participant in match["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant
    return None

def process_last_ten_games(n, output_data, games, players, GAME_NAME, TAG_LINE):
    if not API_KEYS:
        print("ERROR: RIOT_API_KEYS environment variable is not set.")
        
    global current_api_key
    current_api_key += 1
    if current_api_key >= len(API_KEYS) - 1:
        current_api_key = 0
    
    time.sleep(1)

    print(f"Looking up {GAME_NAME}#{TAG_LINE}...")
    print()

    account = get_account(GAME_NAME, TAG_LINE)
    puuid = account["puuid"]

    print(f"Riot ID : {account['gameName']}#{account['tagLine']}")
    print(f"PUUID   : {puuid}")
    print()

    match_ids = get_match_ids(puuid)
    if not match_ids:
        print("No TFT matches found.")
        return

    print(f"Found {len(match_ids)} matches.")
    print("=" * 80)

    for index, match_id in enumerate(match_ids, start=1):
        if match_id in games:
            continue

        if n[0] <= 0:
            return

        games.append(match_id)
        match = get_match(match_id)
        info = match["info"]

        player = find_player(match, puuid)
        if player is None:
            print(f"{index}. {match_id}: player not found")
            continue

        game_datetime = datetime.date.fromtimestamp(
            info["game_datetime"] / 1000
        )

        participants = [f"{participant['puuid']}   win: {participant["win"]}" for participant in info['participants']]

        print(f"{index}. {match_id}")
        print(f"   Date       : {game_datetime}")
        print(f"   Placement  : #{player['placement']}")
        print(f"   Level      : {player['level']}")
        print(f"   Last round : {player['last_round']}")
        print(f"   Players    : \n\t{'\n\t'.join(participants)}")
        print()

        for unit in player['units']:
            unit_name = unit['character_id']
            if not unit_name in output_data.keys():
                output_data[unit_name] = {
                    "unit": unit_name,
                    "count": 0,
                    "place": 0,
                    "wins": 0,
                    "top4": 0,
                    "items": {}
                }

            output_data[unit_name]['place'] += player['placement']
            output_data[unit_name]['count'] += 1
            if player['win'] == True:
                output_data[unit_name]['wins'] += 1
            if 1 <= player['placement'] <= 4:
                output_data[unit_name]['top4'] += 1

            for item in unit['itemNames']:
                if not item in output_data[unit_name]['items'].keys():
                    output_data[unit_name]['items'][item] = 1
                else:
                    output_data[unit_name]['items'][item] += 1
        # recursive
        for participant in info['participants']:
            if participant not in players:
                players.append(f"{participant['riotIdGameName']}#{participant['riotIdTagline']}")
            else:
                continue
            time.sleep(0.5)
            process_last_ten_games([n[0] - 1], output_data, games, players, participant['riotIdGameName'], participant['riotIdTagline'])
    print("Could not find a match")

if __name__ == "__main__":
    output_file = "data.json"
    game_file = "games.json"
    players_file = "players.json"
    data = {}
    games = []
    players = []
    n = [100000]
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
        with open(game_file, 'r') as f:
            games = json.load(f)
        with open(players_file, 'r') as f:
            players = json.load(f)
    except Exception:
        pass
    try:
        process_last_ten_games(n, data, games, players, "fandel", "kahn")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e.with_traceback(None))
    with open(output_file, 'w') as f:
        json.dump(data, f)
    with open(game_file, 'w') as f:
        json.dump(games, f)
    with open(players_file, 'w') as f:
        json.dump(players, f)
