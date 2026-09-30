import { apiGet } from "@/lib/api";


export function getSearchFromQuery(query: string): Promise<any> {
  return apiGet<any>(`/api/search/${query}`);
}
