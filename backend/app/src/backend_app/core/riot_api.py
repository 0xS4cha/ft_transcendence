import logging
from urllib.parse import quote

import httpx

from shared.database import db as database

logger = logging.getLogger(__name__)


class RIOTApi:
    def __init__(self, api_key: str):
        self.API_KEY = api_key.strip()
        self.TIMEOUT_SECONDS = 10

    async def riot_get(self, url: str, server: str, params=None):
        headers = {
            "X-Riot-Token": self.API_KEY,
        }

        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
                response = await client.get(
                    f"https://{server}.api.riotgames.com{url}",
                    headers=headers,
                    params=params,
                )
        except httpx.HTTPError as e:
            logger.warning(f"[riot_get] request failed for {url}: {e!r}")
            return None

        if response.status_code in (401, 403):
            logger.warning(f"[riot_get] {response.status_code}: Riot API key is invalid or expired")
            return None

        if response.status_code != 200:
            return None

        try:
            return response.json()
        except ValueError:
            return None


    async def get_account(self, game_name: str, tag_line: str, server: str):
        return await self.riot_get(f"/riot/account/v1/accounts/by-riot-id/{quote(game_name, safe='')}/{quote(tag_line, safe='')}", server)

    async def get_summoner(self, puuid: str, server: str):
        return await self.riot_get(f"/tft/summoner/v1/summoners/by-puuid/{quote(puuid, safe='')}", server)

    async def get_ranked(self, summoner_id: str, server: str):
        return await self.riot_get(f"/tft/league/v1/by-puuid/{quote(summoner_id, safe='')}", server)

    async def get_region(self, puuid: str):
        response = await self.riot_get(f"/riot/account/v1/region/by-game/tft/by-puuid/{quote(puuid, safe='')}", "europe")
        if not isinstance(response, dict) or not isinstance(response.get("region"), str):
            return None
        return response["region"].upper()


riot_api = RIOTApi(database.settings.RIOT_API_KEY)
