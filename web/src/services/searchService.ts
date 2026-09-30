import { apiGet } from "@/lib/api";


export function refuseFriendRequest(query: string): Promise<any> {
  return apiGet<any>(`/api/search/${query}`);
}
