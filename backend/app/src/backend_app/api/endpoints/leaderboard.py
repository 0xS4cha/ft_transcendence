from http.client import HTTPException
import time
import aiohttp
from fastapi import APIRouter

router = APIRouter()

cache = {}
last_calculated_timestamp = 0
REFRESH_INTERVAL_MS = 20000

@router.get("/")
async def leaderboard_get_top_fifty(server: str = "global"):
	global cache
	global last_calculated_timestamp

	if server.strip().upper() not in ["BR1","EUN1","EUW1","JP1","KR","LA1","LA2","ME1","NA1","OC1","RU","SG2","TR1","TW2","VN2"]:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid server"
		)

	current_time = time.time()
	if current_time - last_calculated_timestamp > REFRESH_INTERVAL_MS:
		async with aiohttp.ClientSession() as session, session.get(f"https://api.metatft.com/tft-leaderboard/v2/{server.lower().strip()}?offset=0&limit=50") as resp:
			json_leaderboard = await resp.json()
			cache = json_leaderboard
			last_calculated_timestamp = current_time

	return cache