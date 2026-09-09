from enum import Enum

from fastapi import APIRouter, HTTPException, status
from backend_app.database import AsyncSessionDep
from backend_app.core.riot_api import riot_api

router = APIRouter()

class Platform(Enum):
	BR1="BR1"
	EUN1="EUN1"
	EUW1="EUW1"
	JP1="JP1"
	KR="KR"
	LA1="LA1"
	LA2="LA2"
	ME1="ME1"
	NA1="NA1"
	OC1="OC1"
	RU="RU"
	SG2="SG2"
	TR1="TR1"
	TW2="TW2"
	VN2="VN2"


class SearchType(Enum):
	unit="UNIT"
	item="ITEM"
	trait="TRAIT"
	player="PLAYER"
	

searched_user_cache = {}
async def query_user_profile(query_username: str, server: Platform):
	if query_username.count('#') == 1:
		if query_username in searched_user_cache:
			return {username: data for username, data in searched_user_cache.items() if username == query_username}

		game_name = query_username.split('#')[0].strip()
		game_tag = query_username.split('#')[1].strip()
		account = riot_api.get_account(game_name, game_tag, server.value)
		if not account or not "puuid" in account:
			return {}

		summoner = riot_api.get_summoner(account["puuid"], server.value)
		if not summoner or not "id" in summoner:
			return {}

		ranked_data = riot_api.get_ranked(summoner["id"], server.value)
		if not ranked_data:
			return {}
		username = f"{account.get('gameName')}#{account.get('tagLine')}"
		searched_user_cache[username] = {
			'id': summoner.get('id'),
			'puuid': summoner.get('puuid'),
			'profileIconId': summoner.get('profileIconId'),
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
	
	

# unit, user, item
@router.get("/{query_type}/{query}")
async def search(query_type: str, query: str, session: AsyncSessionDep):
	query = query.strip()
	try:
		final = {}
		if query_type.count('_') == 1:
			search_type, platform = tuple(query_type.split('_', 2))
			print(search_type, platform)
			final["user"] = await query_user_profile(query.strip(), Platform(platform))
		else:
			search_type = SearchType(query_type)
		return final
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Incorrect username or password {e}"
		)