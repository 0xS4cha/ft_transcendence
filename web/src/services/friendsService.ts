import { apiGet, apiPostLink } from "@/lib/api";
import { type HomeDataProps } from "@/types/home";

export function getFriendsList(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/friends/friends_list");
}

export function getFriendsRequestList(): Promise<HomeDataProps> {
  return apiGet<HomeDataProps>("/api/friends/friend_requests_list");
}

export function sendFriendsRequest(id: string): Promise<HomeDataProps> {
  return apiPostLink<HomeDataProps>(`/api/friends/send_friend_request/${id}`);
}

export function acceptFriendsRequest(id: string): Promise<HomeDataProps> {
  return apiPostLink<HomeDataProps>(`/api/friends/accept_friend_request/${id}`);
}