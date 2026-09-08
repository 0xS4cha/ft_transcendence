import json

from sqlalchemy.orm import Session

from ..shared.models import ProcessedGame, UnitStat


def load_units_in_db(engine):
	game_data = {}
	with open("/opt/game_data/fetch_matches/data.json", 'r') as f:
		game_data = json.load(f)
	game_list = []
	with open("/opt/game_data/fetch_matches/games.json", 'r') as f:
		game_list = json.load(f)
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
		for match_id in game_list:
			session.add(ProcessedGame(
				match_id=match_id
			))
		session.commit()