import os

__env_name = os.getenv("CONTAINER_NAME")
if __env_name:
    if __env_name == "backend":
        from shared.models.unit_games import PerDayStats, ProcessedGame, UnitStat

    else:
        from .unit_games import PerDayStats, ProcessedGame, UnitStat

__all__ = [
    "PerDayStats",
    "ProcessedGame",
    "UnitStat",
]