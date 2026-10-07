import { apiGet, apiPostLink, apiDeleteLink } from "@/lib/api";
import { type UserPublic, type FriendState } from "@/types/user";
import { toast } from "@/components/ui/toast";

export function getFriendsList(): Promise<FriendState[]> {
  return apiGet<FriendState[]>("/api/friends/friends_list");
}

export function getFriendsRequestList(): Promise<UserPublic[]> {
  return apiGet<UserPublic[]>("/api/friends/friend_requests_list");
}

export function sendFriendsRequest(id: string): Promise<any> {
  return apiPostLink<any>(`/api/friends/send_friend_request/${id}`);
}

export function acceptFriendRequest(id: string): Promise<any> {
  return apiPostLink<any>(`/api/friends/accept_friend_request/${id}`);
}

export function removeFriend(id: string): Promise<any> {
  return apiDeleteLink<any>(`/api/friends/remove_friend/${id}`);
}

export function refuseFriendRequest(id: string): Promise<any> {
  return apiDeleteLink<any>(`/api/friends/refuse_friend_request/${id}`);
}

export function receiveFriendRequest(id: string): void {
   const toastId = toast.add({
    title: "Friend request",
    description: `${id} has sent you a friend request`,
    actionProps: {
      children: "Accept",
      onClick() {
        acceptFriendRequest(id)
        toast.close(toastId)
      },
    },
  })
}