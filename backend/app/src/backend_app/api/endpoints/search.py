from enum import Enum

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from backend_app.core.riot_api import riot_api
from backend_app.models.users import UserModel
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

	ranked_data = next(
		(queue for queue in ranked_data_lst if queue.get("queueType") == "RANKED_TFT"),
		ranked_data_lst[0],
	)

	username = f"{account.get('gameName')}#{account.get('tagLine')}"
	searched_user_cache[username] = {
		'id': username,
		'username': username,
		'region': region,
		'puuid': summoner.get('puuid'),
		'picture': f"https://cdn.metatft.com/file/metatft/profileicons/profileicon{summoner.get('profileIconId')}.png",
		'icon': f"https://cdn.metatft.com/file/metatft/profileicons/profileicon{summoner.get('profileIconId')}.png",
		'summonerLevel': summoner.get('summonerLevel'),
		'source': 'riot',
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

async def query_local_users(query: str, session: AsyncSessionDep):
	result = await session.execute(
		select(UserModel)
		.where(UserModel.username.ilike(f"%{query}%"))
		.limit(8)
	)
	users = result.scalars().all()
	return [
		{
			'id': user.id,
			'username': user.username,
			'picture': user.picture,
			'icon': user.picture,
			'source': 'local',
		}
		for user in users
	]

async def query_unit(query: str, session: AsyncSessionDep):
	result = await session.execute(
		select(Unit)
		.where(Unit.name.ilike(f"%{query}%"))
		.limit(8)
	)
	return result.scalars().all()

async def query_item(query: str, session: AsyncSessionDep):
	result = await session.execute(
		select(Item)
		.where((Item.name.ilike(f"%{query}%")) | (Item.id.ilike(f"%{query}%")))
		.limit(8)
	)
	return result.scalars().all()

async def query_trait(query: str, session: AsyncSessionDep):
	result = await session.execute(
		select(Trait)
		.where((Trait.name.ilike(f"%{query}%")) | (Trait.id.ilike(f"%{query}%")))
		.limit(8)
	)
	return result.scalars().all()

async def query_augment(query: str, session: AsyncSessionDep):
	result = await session.execute(
		select(Augment)
		.where((Augment.name.ilike(f"%{query}%")) | (Augment.id.ilike(f"%{query}%")))
		.limit(8)
	)
	return result.scalars().all()
	

# unit, user, item
@router.get("/{query}")
async def search(query: str, session: AsyncSessionDep):
	query = query.strip()
	if not query:
		return {"unit": [], "item": [], "trait": [], "augment": [], "user": []}

	try:
		final = {}
		users = await query_local_users(query, session)
		try:
			riot_user = await query_user_profile(query.strip())
			if riot_user and not any(user.get("username") == riot_user.get("username") for user in users):
				users.insert(0, riot_user)
		except Exception as e:  # noqa: BLE001
			print(e)
		final["user"] = users
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