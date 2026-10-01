import { type UnitRow } from "@/components/units/schema"
import { type ItemRow } from "@/components/items/schema"
import { type AugmentRow } from "@/components/augments/schema"
import { type TraitRow } from "@/components/traits/schema"

export interface UserSearch {
    id?: string | number;
    icon?: string;
    picture?: string;
    username: string;
    source?: "local" | "riot";
    region?: string;
    puuid?: string;
    summonerLevel?: number;
    queueType?: string;
    tier?: string;
    rank?: string;
    leaguePoints?: number;
    wins?: number;
    losses?: number;
    hotStreak?: boolean;
    veteran?: boolean;
    freshBlood?: boolean;
    inactive?: boolean;
}

export interface SearchResult {
    unit: UnitRow[];
    item: ItemRow[];
    augment: AugmentRow[];
    trait: TraitRow[];
    user: UserSearch[];
    length?: number;
}

export type search = SearchResult;