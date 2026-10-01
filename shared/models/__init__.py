import os

__env_name = os.getenv("CONTAINER_NAME")
if __env_name:
    if __env_name == "backend":
        from shared.models.home_stats import PerDayStats, ProcessedGame, UnitStat

    else:
        from .home_stats import PerDayStats, ProcessedGame, UnitStat

__all__ = [
    "PerDayStats",
    "ProcessedGame",
    "UnitStat",
]