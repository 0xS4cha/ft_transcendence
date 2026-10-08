import os

__env_name = os.getenv("CONTAINER_NAME")
if __env_name:
    if __env_name == "backend":
        from shared.models.home_stats import UnitStat

    else:
        from .home_stats import UnitStat

__all__ = [
    "UnitStat",
]