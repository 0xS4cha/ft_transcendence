import { apiGet } from "@/lib/api";
import { type HomeDataProps } from "@/types/home";

export function getHomeStats(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/stats/home");
}
