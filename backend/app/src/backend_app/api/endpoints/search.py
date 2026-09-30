from enum import Enum

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from backend_app.core.riot_api import riot_api
from shared.database import AsyncSessionDep
from shared.models.augments import Augment
from shared.models.items import Item
from shared.models.traits import Trait
from shared.models.units import Unit

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
	

searched_user_cache = {}
async def query_user_profile(query_username: str):
	if query_username.count('#') == 1:
		if query_username in searched_user_cache:
			return {username: data for username, data in searched_user_cache.items() if username == query_username}

		game_name = query_username.split('#')[0].strip()
		game_tag = query_username.split('#')[1].strip()
		account = riot_api.get_account(game_name, game_tag, Platform.JP1.get_continent())
		if not account or not "puuid" in account:
			return {}

		# get region for player
		region = riot_api.get_region(account["puuid"])
		if not region:
			return {}

		server = Platform(region)


		summoner = riot_api.get_summoner(account["puuid"], server.value)
		if not summoner or not "puuid" in summoner:
			return {}

		ranked_data_lst = riot_api.get_ranked(account["puuid"], server.value)
		if not ranked_data_lst or not isinstance(ranked_data_lst, list) or len(ranked_data_lst) == 0:
			return {}

		ranked_data = ranked_data_lst[0]
		
		username = f"{account.get('gameName')}#{account.get('tagLine')}"
		searched_user_cache[username] = {
			'username': username,
			'region': region,
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

async def query_unit(query: str, session: AsyncSessionDep):
	async with session:
		unit_list = (await session.execute(select(Unit))).scalars().all()
		return [unit for unit in unit_list if query.lower().strip() in unit.name.lower().strip()]

async def query_item(query: str, session: AsyncSessionDep):
	async with session:
		item_list = (await session.execute(select(Item))).scalars().all()
		return [item for item in item_list if query.lower().strip() in item.id.lower().strip()]

async def query_trait(query: str, session: AsyncSessionDep):
	async with session:
		trait_list = (await session.execute(select(Trait))).scalars().all()
		return [trait for trait in trait_list if query.lower().strip() in trait.name.lower().strip()]

async def query_augment(query: str, session: AsyncSessionDep):
	async with session:
		augment_list = (await session.execute(select(Augment))).scalars().all()
		return [augment for augment in augment_list if query.lower().strip() in augment.name.lower().strip()]
	

# unit, user, item
@router.get("/{query}")
async def search(query: str, session: AsyncSessionDep):
	query = query.strip()
	try:
		final = {}
		try:
			final["user"] = [await query_user_profile(query.strip())]
		except Exception as e:  # noqa: BLE001
			print(e)
			final["user"] = [] # none found
		final["unit"] = await query_unit(query.strip(), session)
		final["item"] = await query_item(query.strip(), session)
		final["trait"] = await query_trait(query.strip(), session)
		final["augment"] = await query_augment(query.strip(), session)
		return final
	except Exception as e: # noqa: BLE001
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"{e}"
		)