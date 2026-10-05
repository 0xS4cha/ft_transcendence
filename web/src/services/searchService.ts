import { apiGet } from "@/lib/api";
import { type SearchResult } from "@/types/search";

const EMPTY_RESULT: SearchResult = {
  unit: [],
  item: [],
  augment: [],
  trait: [],
  user: [],
};

export async function getSearchFromQuery(query: string): Promise<SearchResult> {
  const result = await apiGet<Partial<SearchResult>>(`/api/search/${encodeURIComponent(query)}`);

  return {
    ...EMPTY_RESULT,
    ...result,
    unit: result.unit ?? [],
    item: result.item ?? [],
    trait: result.trait ?? [],
    augment: result.augment ?? [],
    user: (result.user ?? []).filter((entry) => Boolean(entry?.username)),
  };
}
