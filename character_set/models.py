from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from classes import DetailedChampion


class Base(DeclarativeBase):
    pass


class Champion(Base):
    __tablename__ = "champions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[str] = mapped_column("contentId", String)
    name: Mapped[str] = mapped_column(String)
    alias: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    short_bio: Mapped[str] = mapped_column("shortBio", String)
    is_visible_in_client: Mapped[bool] = mapped_column("isVisibleInClient", Boolean)
    square_portrait_path: Mapped[str] = mapped_column("squarePortraitPath", String)
    stinger_sfx_path: Mapped[str] = mapped_column("stingerSfxPath", String)
    choose_vo_path: Mapped[str] = mapped_column("chooseVoPath", String)
    ban_vo_path: Mapped[str] = mapped_column("banVoPath", String)

    tactical_info: Mapped[TacticalInfo] = relationship(
        back_populates="champion", cascade="all, delete-orphan", uselist=False
    )
    playstyle_info: Mapped[PlaystyleInfo] = relationship(
        back_populates="champion", cascade="all, delete-orphan", uselist=False
    )
    tag_info: Mapped[ChampionTagInfo] = relationship(
        back_populates="champion", cascade="all, delete-orphan", uselist=False
    )
    passive: Mapped[ChampionPassive] = relationship(
        back_populates="champion", cascade="all, delete-orphan", uselist=False
    )
    roles: Mapped[list[ChampionRole]] = relationship(cascade="all, delete-orphan")
    recommended_item_defaults: Mapped[list[RecommendedItemDefault]] = relationship(
        cascade="all, delete-orphan"
    )
    skins: Mapped[list[Skin]] = relationship(cascade="all, delete-orphan")
    spells: Mapped[list[Spell]] = relationship(cascade="all, delete-orphan")


class TacticalInfo(Base):
    __tablename__ = "champion_tactical_info"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    style: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)
    damage_type: Mapped[str] = mapped_column("damageType", String)
    attack_type: Mapped[str] = mapped_column("attackType", String)
    champion: Mapped[Champion] = relationship(back_populates="tactical_info")


class PlaystyleInfo(Base):
    __tablename__ = "champion_playstyle_info"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    damage: Mapped[int] = mapped_column(Integer)
    durability: Mapped[int] = mapped_column(Integer)
    crowd_control: Mapped[int] = mapped_column("crowdControl", Integer)
    mobility: Mapped[int] = mapped_column(Integer)
    utility: Mapped[int] = mapped_column(Integer)
    champion: Mapped[Champion] = relationship(back_populates="playstyle_info")


class ChampionTagInfo(Base):
    __tablename__ = "champion_tag_info"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    champion_tag_primary: Mapped[str] = mapped_column("championTagPrimary", String)
    champion_tag_secondary: Mapped[str] = mapped_column("championTagSecondary", String)
    champion: Mapped[Champion] = relationship(back_populates="tag_info")


class ChampionPassive(Base):
    __tablename__ = "champion_passives"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    ability_icon_path: Mapped[str] = mapped_column("abilityIconPath", String)
    ability_video_path: Mapped[str] = mapped_column("abilityVideoPath", String)
    ability_video_image_path: Mapped[str] = mapped_column("abilityVideoImagePath", String)
    description: Mapped[str] = mapped_column(String)
    champion: Mapped[Champion] = relationship(back_populates="passive")


class ChampionRole(Base):
    __tablename__ = "champion_roles"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String, primary_key=True)


class RecommendedItemDefault(Base):
    __tablename__ = "champion_recommended_item_defaults"

    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), primary_key=True)
    item_id: Mapped[str] = mapped_column("itemId", String, primary_key=True)


class Skin(Base):
    __tablename__ = "skins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), index=True)
    content_id: Mapped[str] = mapped_column("contentId", String)
    is_base: Mapped[bool] = mapped_column("isBase", Boolean)
    name: Mapped[str] = mapped_column(String)
    skin_classification: Mapped[str] = mapped_column("skinClassification", String)
    splash_path: Mapped[str] = mapped_column("splashPath", String)
    uncentered_splash_path: Mapped[str] = mapped_column("uncenteredSplashPath", String)
    tile_path: Mapped[str] = mapped_column("tilePath", String)
    load_screen_path: Mapped[str] = mapped_column("loadScreenPath", String)
    load_screen_vintage_path: Mapped[str | None] = mapped_column("loadScreenVintagePath", String)
    skin_type: Mapped[str] = mapped_column("skinType", String)
    rarity: Mapped[str] = mapped_column(String)
    is_legacy: Mapped[bool] = mapped_column("isLegacy", Boolean)
    splash_video_path: Mapped[str | None] = mapped_column("splashVideoPath", String)
    preview_video_url: Mapped[str | None] = mapped_column("previewVideoUrl", String)
    collection_splash_video_path: Mapped[str | None] = mapped_column("collectionSplashVideoPath", String)
    collection_card_hover_video_path: Mapped[str | None] = mapped_column("collectionCardHoverVideoPath", String)
    features_text: Mapped[str | None] = mapped_column("featuresText", String)
    chroma_path: Mapped[str | None] = mapped_column("chromaPath", String)
    emblems: Mapped[str | None] = mapped_column(String)
    region_rarity_id: Mapped[int] = mapped_column("regionRarityId", Integer)
    rarity_gem_path: Mapped[str | None] = mapped_column("rarityGemPath", String)
    description: Mapped[str | None] = mapped_column(String)

    chromas: Mapped[list[Chroma]] = relationship(cascade="all, delete-orphan")
    skin_lines: Mapped[list[SkinLine]] = relationship(cascade="all, delete-orphan")


class SkinLine(Base):
    __tablename__ = "skin_lines"

    skin_id: Mapped[int] = mapped_column(ForeignKey("skins.id"), primary_key=True)
    line_id: Mapped[int] = mapped_column("lineId", Integer, primary_key=True)


class Chroma(Base):
    __tablename__ = "chromas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skin_id: Mapped[int] = mapped_column(ForeignKey("skins.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    content_id: Mapped[str] = mapped_column("contentId", String)
    related_prime_content_id: Mapped[str] = mapped_column("relatedPrimeContentId", String)
    skin_classification: Mapped[str] = mapped_column("skinClassification", String)
    chroma_path: Mapped[str] = mapped_column("chromaPath", String)
    tile_path: Mapped[str] = mapped_column("tilePath", String)
    colors: Mapped[list[str]] = mapped_column(JSON)
    description: Mapped[str] = mapped_column(String)

    descriptions: Mapped[list[SkinDescription]] = relationship(cascade="all, delete-orphan")
    rarities: Mapped[list[SkinRarity]] = relationship(cascade="all, delete-orphan")


class SkinDescription(Base):
    __tablename__ = "skin_descriptions"

    chroma_id: Mapped[int] = mapped_column(ForeignKey("chromas.id"), primary_key=True)
    region: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str | None] = mapped_column(String)


class SkinRarity(Base):
    __tablename__ = "skin_rarities"

    chroma_id: Mapped[int] = mapped_column(ForeignKey("chromas.id"), primary_key=True)
    region: Mapped[str] = mapped_column(String, primary_key=True)
    rarity: Mapped[int] = mapped_column(Integer)


class Spell(Base):
    __tablename__ = "spells"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    champion_id: Mapped[int] = mapped_column(ForeignKey("champions.id"), index=True)
    spell_key: Mapped[str] = mapped_column("spellKey", String)
    name: Mapped[str] = mapped_column(String)
    ability_icon_path: Mapped[str] = mapped_column("abilityIconPath", String)
    ability_video_path: Mapped[str] = mapped_column("abilityVideoPath", String)
    ability_video_image_path: Mapped[str] = mapped_column("abilityVideoImagePath", String)
    cost: Mapped[str] = mapped_column(String)
    cooldown: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    dynamic_description: Mapped[str] = mapped_column("dynamicDescription", String)
    range_values: Mapped[list[float]] = mapped_column("range", JSON)
    cost_coefficients: Mapped[list[float]] = mapped_column("costCoefficients", JSON)
    cooldown_coefficients: Mapped[list[float]] = mapped_column("cooldownCoefficients", JSON)
    max_level: Mapped[int] = mapped_column("maxLevel", Integer)

    coefficients: Mapped[SpellCoefficients] = relationship(cascade="all, delete-orphan", uselist=False)
    effect_amounts: Mapped[SpellEffectAmounts] = relationship(cascade="all, delete-orphan", uselist=False)
    ammo: Mapped[SpellAmmo] = relationship(cascade="all, delete-orphan", uselist=False)


class SpellCoefficients(Base):
    __tablename__ = "spell_coefficients"

    spell_id: Mapped[int] = mapped_column(ForeignKey("spells.id"), primary_key=True)
    coefficient1: Mapped[float] = mapped_column()
    coefficient2: Mapped[float] = mapped_column()


class SpellEffectAmounts(Base):
    __tablename__ = "spell_effect_amounts"

    spell_id: Mapped[int] = mapped_column(ForeignKey("spells.id"), primary_key=True)
    effect1_amount: Mapped[list[float]] = mapped_column("Effect1Amount", JSON)
    effect2_amount: Mapped[list[float]] = mapped_column("Effect2Amount", JSON)
    effect3_amount: Mapped[list[float]] = mapped_column("Effect3Amount", JSON)
    effect4_amount: Mapped[list[float]] = mapped_column("Effect4Amount", JSON)
    effect5_amount: Mapped[list[float]] = mapped_column("Effect5Amount", JSON)
    effect6_amount: Mapped[list[float]] = mapped_column("Effect6Amount", JSON)
    effect7_amount: Mapped[list[float]] = mapped_column("Effect7Amount", JSON)
    effect8_amount: Mapped[list[float]] = mapped_column("Effect8Amount", JSON)
    effect9_amount: Mapped[list[float]] = mapped_column("Effect9Amount", JSON)
    effect10_amount: Mapped[list[float]] = mapped_column("Effect10Amount", JSON)


class SpellAmmo(Base):
    __tablename__ = "spell_ammo"

    spell_id: Mapped[int] = mapped_column(ForeignKey("spells.id"), primary_key=True)
    ammo_recharge_time: Mapped[list[float]] = mapped_column("ammoRechargeTime", JSON)
    max_ammo: Mapped[list[float]] = mapped_column("maxAmmo", JSON)


def champion_from_payload(payload: DetailedChampion) -> Champion:
    champion = Champion(
        id=payload.id, content_id=payload.contentId, name=payload.name, alias=payload.alias,
        title=payload.title, short_bio=payload.shortBio,
        is_visible_in_client=payload.isVisibleInClient,
        square_portrait_path=payload.squarePortraitPath, stinger_sfx_path=payload.stingerSfxPath,
        choose_vo_path=payload.chooseVoPath, ban_vo_path=payload.banVoPath,
        tactical_info=TacticalInfo(
            style=payload.tacticalInfo.style, difficulty=payload.tacticalInfo.difficulty,
            damage_type=payload.tacticalInfo.damageType, attack_type=payload.tacticalInfo.attackType,
        ),
        playstyle_info=PlaystyleInfo(
            damage=payload.playstyleInfo.damage, durability=payload.playstyleInfo.durability,
            crowd_control=payload.playstyleInfo.crowdControl, mobility=payload.playstyleInfo.mobility,
            utility=payload.playstyleInfo.utility,
        ),
        tag_info=ChampionTagInfo(
            champion_tag_primary=payload.championTagInfo.championTagPrimary,
            champion_tag_secondary=payload.championTagInfo.championTagSecondary,
        ),
        passive=ChampionPassive(
            name=payload.passive.name, ability_icon_path=payload.passive.abilityIconPath,
            ability_video_path=payload.passive.abilityVideoPath,
            ability_video_image_path=payload.passive.abilityVideoImagePath,
            description=payload.passive.description,
        ),
        roles=[ChampionRole(role=role) for role in payload.roles],
        recommended_item_defaults=[RecommendedItemDefault(item_id=item) for item in payload.recommendedItemDefaults],
    )
    for payload_skin in payload.skins:
        skin = Skin(
            id=payload_skin.id, content_id=payload_skin.contentId, is_base=payload_skin.isBase,
            name=payload_skin.name, skin_classification=payload_skin.skinClassification,
            splash_path=payload_skin.splashPath, uncentered_splash_path=payload_skin.uncenteredSplashPath,
            tile_path=payload_skin.tilePath, load_screen_path=payload_skin.loadScreenPath,
            load_screen_vintage_path=payload_skin.loadScreenVintagePath, skin_type=payload_skin.skinType,
            rarity=payload_skin.rarity, is_legacy=payload_skin.isLegacy,
            splash_video_path=payload_skin.splashVideoPath, preview_video_url=payload_skin.previewVideoUrl,
            collection_splash_video_path=payload_skin.collectionSplashVideoPath,
            collection_card_hover_video_path=payload_skin.collectionCardHoverVideoPath,
            features_text=payload_skin.featuresText, chroma_path=payload_skin.chromaPath,
            emblems=payload_skin.emblems, region_rarity_id=payload_skin.regionRarityId,
            rarity_gem_path=payload_skin.rarityGemPath, description=payload_skin.description,
            skin_lines=[SkinLine(line_id=line.id) for line in payload_skin.skinLines or []],
        )
        for payload_chroma in payload_skin.chromas:
            skin.chromas.append(Chroma(
                id=payload_chroma.id, name=payload_chroma.name, content_id=payload_chroma.contentId,
                related_prime_content_id=payload_chroma.relatedPrimeContentId,
                skin_classification=payload_chroma.skinClassification, chroma_path=payload_chroma.chromaPath,
                tile_path=payload_chroma.tilePath, colors=payload_chroma.colors,
                description=payload_chroma.description,
                descriptions=[SkinDescription(**description.model_dump()) for description in payload_chroma.descriptions],
                rarities=[SkinRarity(**rarity.model_dump()) for rarity in payload_chroma.rarities],
            ))
        champion.skins.append(skin)
    for payload_spell in payload.spells:
        champion.spells.append(Spell(
            spell_key=payload_spell.spellKey, name=payload_spell.name,
            ability_icon_path=payload_spell.abilityIconPath, ability_video_path=payload_spell.abilityVideoPath,
            ability_video_image_path=payload_spell.abilityVideoImagePath, cost=payload_spell.cost,
            cooldown=payload_spell.cooldown, description=payload_spell.description,
            dynamic_description=payload_spell.dynamicDescription, range_values=payload_spell.range,
            cost_coefficients=payload_spell.costCoefficients,
            cooldown_coefficients=payload_spell.cooldownCoefficients, max_level=payload_spell.maxLevel,
            coefficients=SpellCoefficients(**payload_spell.coefficients.model_dump()),
            effect_amounts=SpellEffectAmounts(
                effect1_amount=payload_spell.effectAmounts.Effect1Amount, effect2_amount=payload_spell.effectAmounts.Effect2Amount,
                effect3_amount=payload_spell.effectAmounts.Effect3Amount, effect4_amount=payload_spell.effectAmounts.Effect4Amount,
                effect5_amount=payload_spell.effectAmounts.Effect5Amount, effect6_amount=payload_spell.effectAmounts.Effect6Amount,
                effect7_amount=payload_spell.effectAmounts.Effect7Amount, effect8_amount=payload_spell.effectAmounts.Effect8Amount,
                effect9_amount=payload_spell.effectAmounts.Effect9Amount, effect10_amount=payload_spell.effectAmounts.Effect10Amount,
            ),
            ammo=SpellAmmo(ammo_recharge_time=payload_spell.ammo.ammoRechargeTime, max_ammo=payload_spell.ammo.maxAmmo),
        ))
    return champion
