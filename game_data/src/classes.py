from typing import List
from pydantic import Field, BaseModel


class ChampionSummaryItem(BaseModel):
    id: int
    name: str
    description: str
    alias: str
    contentId: str
    squarePortraitPath: str
    roles: List[str]

class SkinLine(BaseModel):
    id: int


class SkinDescription(BaseModel):
    region: str
    description: str | None


class SkinRarity(BaseModel):
    region: str
    rarity: int


class Chroma(BaseModel):
    id: int
    name: str
    contentId: str
    relatedPrimeContentId: str
    skinClassification: str
    chromaPath: str
    tilePath: str
    colors: List[str]
    descriptions: List[SkinDescription]
    description: str
    rarities: List[SkinRarity]


class Skin(BaseModel):
    id: int
    contentId: str
    isBase: bool
    name: str
    skinClassification: str
    splashPath: str
    uncenteredSplashPath: str
    tilePath: str
    loadScreenPath: str
    loadScreenVintagePath: str | None = None
    skinType: str
    rarity: str
    isLegacy: bool

    splashVideoPath: str | None = None
    previewVideoUrl: str | None = None
    collectionSplashVideoPath: str | None = None
    collectionCardHoverVideoPath: str | None = None
    featuresText: str | None = None

    chromaPath: str | None = None
    chromas: List[Chroma] = []

    emblems: str | None = None
    regionRarityId: int
    rarityGemPath: str | None = None

    skinLines: List[SkinLine] | None = []
    description: str | None


class SpellCoefficients(BaseModel):
    coefficient1: float
    coefficient2: float


class SpellEffectAmounts(BaseModel):
    Effect1Amount: List[float]
    Effect2Amount: List[float]
    Effect3Amount: List[float]
    Effect4Amount: List[float]
    Effect5Amount: List[float]
    Effect6Amount: List[float]
    Effect7Amount: List[float]
    Effect8Amount: List[float]
    Effect9Amount: List[float]
    Effect10Amount: List[float]


class SpellAmmo(BaseModel):
    ammoRechargeTime: List[float]
    maxAmmo: List[float]


class Spell(BaseModel):
    spellKey: str
    name: str
    abilityIconPath: str
    abilityVideoPath: str
    abilityVideoImagePath: str
    cost: str
    cooldown: str
    description: str
    dynamicDescription: str

    range: List[float]
    costCoefficients: List[float]
    cooldownCoefficients: List[float]

    coefficients: SpellCoefficients
    effectAmounts: SpellEffectAmounts
    ammo: SpellAmmo

    maxLevel: int

class TacticalInfo(BaseModel):
    style: int
    difficulty: int
    damageType: str
    attackType: str


class PlaystyleInfo(BaseModel):
    damage: int
    durability: int
    crowdControl: int
    mobility: int
    utility: int


class ChampionTagInfo(BaseModel):
    championTagPrimary: str
    championTagSecondary: str


class ChampionPassive(BaseModel):
    name: str
    abilityIconPath: str
    abilityVideoPath: str
    abilityVideoImagePath: str
    description: str


class DetailedChampion(BaseModel):
    id: int
    contentId: str
    name: str
    alias: str
    title: str
    shortBio: str

    isVisibleInClient: bool

    tacticalInfo: TacticalInfo
    playstyleInfo: PlaystyleInfo
    championTagInfo: ChampionTagInfo

    squarePortraitPath: str
    stingerSfxPath: str
    chooseVoPath: str
    banVoPath: str

    roles: List[str]
    recommendedItemDefaults: List[str]

    skins: List[Skin] = Field(default_factory=list)

    passive: ChampionPassive

    spells: List[Spell] = Field(default_factory=list)