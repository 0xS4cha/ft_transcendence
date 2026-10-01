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
        from shared.models.unit_games import PerDayStats, ProcessedGame, UnitStat

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
        from .unit_games import PerDayStats, ProcessedGame, UnitStat

__all__ = [
    "Champion",
    "ChampionPassive",
    "ChampionRole",
    "ChampionTagInfo",
    "Chroma",
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
    "UnitStat",
]