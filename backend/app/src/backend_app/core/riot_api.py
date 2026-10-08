import asyncio

import httpx

from shared.database import db as database


class RIOTApi:
    def __init__(self, api_key: str):
        self.API_RETRIES = 5
        self.API_KEY = api_key.strip()

    async def riot_get(self, url: str, server: str, params=None):
        headers = {
            "X-Riot-Token": self.API_KEY,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            for _ in range(self.API_RETRIES):
                try:
                    response = await client.get(
                        f"https://{server}.api.riotgames.com{url}",
                        headers=headers,
                        params=params,
                    )

                    if response.status_code in (401, 403):
                        raise Exception(f"{response.status_code} Forbidden: your Riot API key is invalid or expired.") # noqa: TRY002

                    if response.status_code == 404:
                        print(f"https://{server}.api.riotgames.com{url}")
                        raise Exception(f"404 Not Found: {url}")  # noqa: TRY002

                    if response.status_code == 429:
                        raise ConnectionAbortedError(
                            "429 Rate Limited: too many requests."
                        )

                    return response.json()

                except ConnectionAbortedError:
                    print("Retrying in 30s to reset rate limit...")
                    await asyncio.sleep(30)
        return None


    async def get_account(self, game_name: str, tag_line: str, server: str):
        return await self.riot_get(f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}", server)

    async def get_summoner(self, puuid: str, server: str):
        return await self.riot_get(f"/tft/summoner/v1/summoners/by-puuid/{puuid}", server)

    async def get_ranked(self, summoner_id: str, server: str):
        return await self.riot_get(f"/tft/league/v1/by-puuid/{summoner_id}", server)

    async def get_region(self, puuid: str):
        response = await self.riot_get(f"/riot/account/v1/region/by-game/tft/by-puuid/{puuid}", "europe")
        if not response or not isinstance(response, dict) or "region" not in response:
            return None
        return (response["region"] or "").upper()
        

riot_api = RIOTApi(database.settings.RIOT_API_KEY)
