import time

import aiohttp
from fastapi import APIRouter

router = APIRouter()

cache = {}
last_calculated_timestamp = 0
REFRESH_INTERVAL_MS = 20000

@router.get("/")
async def leaderboard_get_top_fifty():
	global cache
	global last_calculated_timestamp

	current_time = time.time()
	if current_time - last_calculated_timestamp > REFRESH_INTERVAL_MS:
		async with aiohttp.ClientSession() as session, session.get("https://api.metatft.com/tft-leaderboard/v2/global?offset=0&limit=50") as resp:
			json_leaderboard = await resp.json()
			cache = json_leaderboard
			last_calculated_timestamp = current_time

	return cache