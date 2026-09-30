import { type UnitRow } from "@/components/units/schema"
import { type ItemRow } from "@/components/items/schema"
import { type AugmentRow } from "@/components/augments/schema"
import { type TraitRow } from "@/components/traits/schema"

export interface userSearch {
    icon: string;
    username: string;
    region: string;
    puuid: string;
    summonerLevel: number;
    queueType: string;
    tier: string;
    rank: string;
    leaguePoints: number;
    wins: number;
    losses: number;
    hotStreak: boolean;
    veteran: boolean;
    freshBlood: boolean;
    inactive: boolean;
}

export interface search {
    unit: UnitRow[];
    item: ItemRow[];
    augment: AugmentRow[];
    trait: TraitRow[];
    user: userSearch[];
    length: number;
}