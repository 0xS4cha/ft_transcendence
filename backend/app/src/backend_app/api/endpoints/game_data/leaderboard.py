import logging
import time

import aiohttp
from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter()

SERVERS = ["GLOBAL", "BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "ME1", "NA1", "OC1", "RU", "SG2", "TR1", "TW2", "VN2"]
REFRESH_INTERVAL_SECONDS = 20
UPSTREAM_TIMEOUT_SECONDS = 10

cache: dict[str, tuple[float, object]] = {}


async def fetch_leaderboard(server_id: str) -> object:
	url = f"https://api.metatft.com/tft-leaderboard/v2/{server_id}?offset=0&limit=50"
	timeout = aiohttp.ClientTimeout(total=UPSTREAM_TIMEOUT_SECONDS)
	async with aiohttp.ClientSession(timeout=timeout) as session, session.get(url) as resp:
		if resp.status != 200:
			raise aiohttp.ClientResponseError(
				resp.request_info, resp.history, status=resp.status
			)
		return await resp.json()


@router.get("/")
async def leaderboard_get_top_fifty(server: str = "global"):
	if server.strip().upper() not in SERVERS:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid server"
		)

	server_id = server.lower().strip()
	current_time = time.time()
	cached = cache.get(server_id)
	if cached is not None and current_time - cached[0] <= REFRESH_INTERVAL_SECONDS:
		return cached[1]

	try:
		data = await fetch_leaderboard(server_id)
	except (TimeoutError, aiohttp.ClientError, ValueError) as e:
		logger.warning(f"[leaderboard] upstream error for {server_id}: {e!r}")
		if cached is not None:
			return cached[1]
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail="Leaderboard unavailable"
		) from e

	if not isinstance(data, (dict, list)) or (isinstance(data, dict) and "error" in data):
		if cached is not None:
			return cached[1]
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail="Leaderboard unavailable"
		)

	cache[server_id] = (current_time, data)
	return data
