import { apiGet } from "@/lib/api";
import { type HomeDataProps } from "@/types/home";
import { type ItemRow } from "@/components/items/schema"
import { type UnitRow } from "@/components/units/schema"
import { type TraitRow } from "@/components/traits/schema"
import { type AugmentRow } from "@/components/augments/schema";

export function getHomeStats(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/stats/home");
}

export function getItemsStats(): Promise<ItemRow[]> {
  return apiGet<ItemRow[]>("/api/game_data/items_data");
}

export function getUnitsStats(): Promise<UnitRow[]> {
  return apiGet<UnitRow[]>("/api/game_data/units_data")
}

export function getTraitsStats(): Promise<TraitRow[]> {
  return apiGet<TraitRow[]>("/api/game_data/traits_data")
}

export function getAugmentsStats(): Promise<AugmentRow[]> {
  return apiGet<AugmentRow[]>("/api/game_data/augments_data")
}