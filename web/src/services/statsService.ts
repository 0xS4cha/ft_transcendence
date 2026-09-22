import { apiGet } from "@/lib/api";
import { type HomeDataProps } from "@/types/home";
import { type Item } from "@/types/item"
import { type Unit } from "@/types/unit"

export function getHomeStats(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/stats/home");
}

export function getItemsStats(): Promise<Item[]> {
  return apiGet<Item[]>("/api/game_data/items_data");
}

export function getUnitsStats(): Promise<Unit[]> {
  return apiGet<Unit[]>("/api/game_data/units_data")
}