import { apiGet } from "@/lib/api";
import { type HomeDataProps } from "@/types/home";
import { type ItemRow } from "@/components/items/schema";
import { type UnitRow } from "@/components/units/schema";
import { type TraitRow } from "@/components/traits/schema";
import { type AugmentRow } from "@/components/augments/schema";
import { type rankingApi } from "@/types/ranking";

export function getHomeStats(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/stats/home");
}

export function getItemsStats(queue = "1100", rank = "DIAMOND", server = "EUW1"): Promise<ItemRow[]> {
  return apiGet<ItemRow[]>(`/api/game_data/items_data?queue=${queue}&rank=${rank}&server=${server}`);
}

export function getUnitsStats(queue = "1100", rank = "DIAMOND", server = "EUW1"): Promise<UnitRow[]> {
  return apiGet<UnitRow[]>(`/api/game_data/units_data?queue=${queue}&rank=${rank}&server=${server}`);
}

export function getTraitsStats(queue = "1100", rank = "DIAMOND", server = "EUW1"): Promise<TraitRow[]> {
  return apiGet<TraitRow[]>(`/api/game_data/traits_data?queue=${queue}&rank=${rank}&server=${server}`);
}

export function getAugmentsStats(queue = "1100", rank = "DIAMOND", server = "EUW1"): Promise<AugmentRow[]> {
  return apiGet<AugmentRow[]>(`/api/game_data/augments_data?queue=${queue}&rank=${rank}&server=${server}`);
}

export function getLeaderboardStats(server = "EUW1"): Promise<rankingApi> {
  // console.log(server);
  // return apiGet<rankingApi>(`/api/leaderboard/`);
  return apiGet<rankingApi>(`/api/leaderboard?server=${server}`);
}