
from pydantic import BaseModel, Field


class ChampionSummaryItem(BaseModel):
    id: int
    name: str
    description: str
    alias: str
    contentId: str
    squarePortraitPath: str
    roles: list[str]

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
    colors: list[str]
    descriptions: list[SkinDescription]
    description: str
    rarities: list[SkinRarity]


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
    chromas: list[Chroma] = []

    emblems: str | None = None
    regionRarityId: int
    rarityGemPath: str | None = None

    skinLines: list[SkinLine] | None = []
    description: str | None


class SpellCoefficients(BaseModel):
    coefficient1: float
    coefficient2: float


class SpellEffectAmounts(BaseModel):
    Effect1Amount: list[float]
    Effect2Amount: list[float]
    Effect3Amount: list[float]
    Effect4Amount: list[float]
    Effect5Amount: list[float]
    Effect6Amount: list[float]
    Effect7Amount: list[float]
    Effect8Amount: list[float]
    Effect9Amount: list[float]
    Effect10Amount: list[float]


class SpellAmmo(BaseModel):
    ammoRechargeTime: list[float]
    maxAmmo: list[float]


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

    range: list[float]
    costCoefficients: list[float]
    cooldownCoefficients: list[float]

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

    roles: list[str]
    recommendedItemDefaults: list[str]

    skins: list[Skin] = Field(default_factory=list)

    passive: ChampionPassive

    spells: list[Spell] = Field(default_factory=list)