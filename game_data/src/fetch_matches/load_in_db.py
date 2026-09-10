import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..shared.models.unit_games import PerDayStats, ProcessedGame, UnitStat


def load_units_in_db(engine):
	game_data = {}
	with open("/opt/game_data/fetch_matches/data.json", 'r') as f:
		game_data = json.load(f)
	game_list = []
	with open("/opt/game_data/fetch_matches/games.json", 'r') as f:
		game_list = json.load(f)
	per_game_stats = []
	with open("/opt/game_data/fetch_matches/per_day_stats.json", 'r') as f:
		per_game_stats = json.load(f)
	i = 0
	with Session(engine) as session:
		for unit_name, unit_data in game_data.items():
			existing = session.get(UnitStat, unit_name)
			if existing is not None:
				session.delete(existing)
				session.flush()
			session.add(UnitStat(
				unit=unit_name,
				count=unit_data.get("count", 0),
				place=unit_data.get("place", 0),
				wins=unit_data.get("wins", 0),
				top4=unit_data.get("top4", 0),
				items=unit_data.get("items", {})
			))
			i += 1
		print(f"Saved \033[35m{i}\033[0m processed games units stats in database")
		session.commit()

		# add processed game list
		existing_ids = set(
			session.execute(
				select(ProcessedGame.match_id).where(
					ProcessedGame.match_id.in_(game_list)
				)
			).scalars().all()
		)
		i = 0
		for match_id in game_list:
			if match_id not in existing_ids:
				session.add(ProcessedGame(
					match_id=match_id
				))
				i+=1
		session.commit()
		print(f"Saved {i} matches in db")

		# add per day stats
		i = 0
		for date, v in per_game_stats.items():
			stats = session.execute(
				select(PerDayStats).where(
					PerDayStats.date == date
				)
			).scalar_one_or_none()

			if stats:
				stats.goldWasted = v.get("goldWasted", 0)
				stats.totalGames = v.get("totalGames", 0)
				stats.totalGameLength = v.get("totalGameLength", 0)
			else:
				session.add(
					PerDayStats(
						date=date,
						goldWasted=v.get("goldWasted", 0),
						totalGames=v.get("totalGames", 0),
						totalGameLength=v.get("totalGameLength", 0)
					)
				)
			i+=1
		session.commit()
		print(f"Saved {i} days stats in db")