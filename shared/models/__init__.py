import os

__env_name = os.getenv("CONTAINER_NAME")
if __env_name:
    if __env_name == "backend":
        from shared.models.champions import (
            Champion,
            ChampionPassive,
            ChampionRole,
            ChampionTagInfo,
            Chroma,
            PlaystyleInfo,
            RecommendedItemDefault,
            Skin,
            SkinDescription,
            SkinLine,
            SkinRarity,
            Spell,
            SpellAmmo,
            SpellCoefficients,
            SpellEffectAmounts,
            TacticalInfo,
        )
        from shared.models.items import Item
        from shared.models.unit_games import PerDayStats, ProcessedGame, UnitStat
        from shared.models.traits import Trait
        from shared.models.units import Unit
    else:
        from .champions import (
            Champion,
            ChampionPassive,
            ChampionRole,
            ChampionTagInfo,
            Chroma,
            PlaystyleInfo,
            RecommendedItemDefault,
            Skin,
            SkinDescription,
            SkinLine,
            SkinRarity,
            Spell,
            SpellAmmo,
            SpellCoefficients,
            SpellEffectAmounts,
            TacticalInfo,
        )
        from .items import Item
        from .unit_games import PerDayStats, ProcessedGame, UnitStat
        from .traits import Trait
        from .units import Unit

__all__ = [
    "Champion",
    "ChampionPassive",
    "ChampionRole",
    "ChampionTagInfo",
    "Chroma",
    "Item",
    "PerDayStats",
    "PlaystyleInfo",
    "ProcessedGame",
    "RecommendedItemDefault",
    "Skin",
    "SkinDescription",
    "SkinLine",
    "SkinRarity",
    "Spell",
    "SpellAmmo",
    "SpellCoefficients",
    "SpellEffectAmounts",
    "TacticalInfo",
    "Trait",
    "Unit",
    "UnitStat",
]