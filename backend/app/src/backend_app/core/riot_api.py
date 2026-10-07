import time
import requests
from shared.database import db as database


class RIOTApi:
    def __init__(self, api_key: str):
        self.API_RETRIES = 5
        self.API_KEY = api_key.strip()

    def riot_get(self, url: str, server: str, params=None):
        for _ in range(self.API_RETRIES):
            response = None
            try:
                headers = {
                    "X-Riot-Token": self.API_KEY,
                }

                response = requests.get(
                    f"https://{server}.api.riotgames.com{url}",
                    headers=headers,
                    params=params,
                    timeout=10,
                )
                if response.status_code == 403 or response.status_code == 401:
                    raise Exception(f"{response.status_code} Forbidden: your Riot API key is invalid or expired.") #noqa: TRY002

                if response.status_code == 404:
                    print(f"https://{server}.api.riotgames.com{url}")
                    raise Exception(f"404 Not Found: {url}") #noqa: TRY002

                if response.status_code == 429:
                    raise ConnectionAbortedError("429 Rate Limited: too many requests.")

                return response.json()
            except ConnectionAbortedError:
                print("Retrying in 30s to reset rate limit...")
                time.sleep(30)
        return None


    def get_account(self, game_name: str, tag_line: str, server: str):
        return self.riot_get(f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}", server)

    def get_summoner(self, puuid: str, server: str):
        return self.riot_get(f"/tft/summoner/v1/summoners/by-puuid/{puuid}", server)

    def get_ranked(self, summoner_id: str, server: str):
        return self.riot_get(f"/tft/league/v1/by-puuid/{summoner_id}", server)

    def get_region(self, puuid: str):
        response = self.riot_get(f"/riot/account/v1/region/by-game/tft/by-puuid/{puuid}", "europe")
        if not response or not isinstance(response, dict) or not "region" in response:
            return None
        return (response["region"] or "").upper()
        

riot_api = RIOTApi(database.settings.RIOT_API_KEY)
