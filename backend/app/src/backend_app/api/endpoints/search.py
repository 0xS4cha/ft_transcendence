from enum import Enum

import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, status

from backend_app.core.dependencies import RedisDep
from backend_app.core.riot_api import riot_api
from backend_app.services.fetch_game_data import build_cache_key, get_or_fetch
from backend_app.services.get_augments import (
	AugmentsUnavailableError,
	augments_adapter,
	get_augments,
)
from backend_app.services.get_items import (
	ItemsUnavailableError,
	get_items,
	items_adapter,
)
from backend_app.services.get_traits import (
	TraitsUnavailableError,
	get_traits,
	traits_adapter,
)
from backend_app.services.get_units import (
	UnitsUnavailableError,
	get_units,
	units_adapter,
)

router = APIRouter()

class Platform(Enum):
	EUN1="EUN1"
	EUW1="EUW1"
	BR1="BR1"
	TR1="TR1"
	
	JP1="JP1"
	RU="RU"
	TW2="TW2"
	OC1="OC1"
	SG2="SG2"
	KR="KR"
	VN2="VN2"


	LA1="LA1"
	LA2="LA2"
	ME1="ME1"
	NA1="NA1"
	
	def get_continent(self):
		if self.value in [Platform.EUN1, Platform.EUW1, Platform.BR1, Platform.TR1]: # europe
			return "europe"
		if self.value in [Platform.JP1, Platform.RU, Platform.TW2, Platform.OC1, Platform.SG2, Platform.KR, Platform.VN2]: # asia
			return "asia"
		if self.value in [Platform.LA1, Platform.LA2, Platform.ME1, Platform.NA1]: # america
			return "america"
		return "europe" # eu by default

queue = "1100"
ranks = "BRONZE,CHALLENGER,DIAMOND,EMERALD,GOLD,GRANDMASTER,IRON,MASTER,PLATINUM,RANKUNKNOWN,SILVER"
servers= "BR1,EUN1,EUW1,JP1,KR,LA1,LA2,ME1,NA1,OC1,RU,SG2,TR1,TW2,VN2"	

searched_user_cache = {}
async def query_user_profile(query_username: str):
	if query_username.count('#') != 1:
		return None

	if query_username in searched_user_cache:
		return searched_user_cache[query_username]

	game_name = query_username.split('#')[0].strip()
	game_tag = query_username.split('#')[1].strip()
	account = riot_api.get_account(game_name, game_tag, Platform.JP1.get_continent())
	if not account or not "puuid" in account:
		return None

	# get region for player
	region = riot_api.get_region(account["puuid"])
	if not region:
		return None

	server = Platform(region)

	summoner = riot_api.get_summoner(account["puuid"], server.value)
	if not summoner or not "puuid" in summoner:
		return None

	ranked_data_lst = riot_api.get_ranked(account["puuid"], server.value)
	if not ranked_data_lst or not isinstance(ranked_data_lst, list) or len(ranked_data_lst) == 0:
		return None

		ranked_data = ranked_data_lst[0]
		
		username = f"{account.get('gameName')}#{account.get('tagLine')}"
		searched_user_cache[username] = {
			'username': username,
			'region': region,
			'puuid': summoner.get('puuid'),
			'icon': f"https://cdn.metatft.com/file/metatft/profileicons/profileicon{summoner.get('profileIconId')}.png",
			'summonerLevel': summoner.get('summonerLevel'),
			"queueType": ranked_data.get('queueType'),
			"tier": ranked_data.get('tier'),
			"rank": ranked_data.get('rank'),
			"leaguePoints": ranked_data.get('leaguePoints'),
			"wins": ranked_data.get('wins'),
			"losses": ranked_data.get('losses'),
			"hotStreak": ranked_data.get('hotStreak'),
			"veteran": ranked_data.get('veteran'),
			"freshBlood": ranked_data.get('freshBlood'),
			"inactive": ranked_data.get('inactive')
		}
		return searched_user_cache[username]
	else:
		return {}


async def query_augment(
	r: redis.Redis,
	query: str,
):
	key = "metatft:augments"

	try:
		augments = await get_or_fetch(r, key, augments_adapter, lambda: get_augments(r))
	except AugmentsUnavailableError as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=str(e)
		) from e

	q = query.lower()
	return [augment for augment in augments if q in augment.name.lower()]


async def query_unit(
	r: redis.Redis,
	query: str,
):
	units_key = build_cache_key("units", queue, ranks, servers)
	traits_key = build_cache_key("traits", queue, ranks, servers)
		
	try:
		traits = await get_or_fetch(r, traits_key, traits_adapter, lambda: get_traits(r, queue, ranks, servers))
		units = await get_or_fetch(r, units_key, units_adapter, lambda: get_units(r, queue, ranks, servers, traits))
	except (TraitsUnavailableError, UnitsUnavailableError)  as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=str(e)
		) from e

	q = query.lower()
	return [unit for unit in units if q in unit.name.lower()]


async def query_item(
	r: redis.Redis,
	query: str
):
	key = build_cache_key("items", queue, ranks, servers)
	
	try:
		items = await get_or_fetch(r, key, items_adapter, lambda: get_items(r, queue, ranks, servers))
	except ItemsUnavailableError as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=str(e)
		) from e

	q = query.lower()
	return [item for item in items if q in item.name.lower()]


async def query_trait(
	r: redis.Redis,
	query: str
):
	key = build_cache_key("traits", queue, ranks, servers)
	
	try:
		traits = await get_or_fetch(r, key, traits_adapter, lambda: get_traits(r, queue, ranks, servers))
	except TraitsUnavailableError as e:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=str(e)
		) from e

	matched = {}
	q = query.lower()

	for trait in traits:
		name = trait.name.lower()
		if q in name and name not in matched:
			matched[name] = trait

	return list(matched.values())


@router.get("/{query}")
async def search(
	query: str,
	r: RedisDep
):
	query = query.strip()
	final = {}

	for key, fn in [
		("unit", query_unit),
		("item", query_item),
		("trait", query_trait),
		("augment", query_augment),
	]:
		try:
			final[key] = await (fn(r, query))
		except HTTPException as e:
			print(f"{key} unavailable: {e.detail}")
			final[key] = []
			
	try:
		final["user"] = [await query_user_profile(query)]
	except Exception as e: #noqa
		print(f"[search] user lookup failed for {query}: {e}")
		final["user"] = []

	return final

	