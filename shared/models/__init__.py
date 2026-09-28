import os

__env_name = os.getenv("CONTAINER_NAME")
if __env_name:
    if __env_name == "backend":
        from shared.models.augments import Augment
        from shared.models.items import Item
        from shared.models.traits import Trait
        from shared.models.unit_games import PerDayStats, ProcessedGame, UnitStat
        from shared.models.units import Unit
    else:
        from .augments import Augment
        from .items import Item
        from .traits import Trait
        from .unit_games import PerDayStats, ProcessedGame, UnitStat
        from .units import Unit

__all__ = [
    "Augment",
    "Item",
    "PerDayStats",
    "ProcessedGame",
    "Trait",
    "Unit",
    "UnitStat",
]