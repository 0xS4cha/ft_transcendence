import { apiGet, apiPostLink, apiDelete } from "@/lib/api";
import { type UserProfile, type FriendState } from "@/types/user";
import { toast } from "@/components/ui/toast";

export function getFriendsList(): Promise<FriendState[]> {
  return apiGet<FriendState[]>("/api/friends/friends_list");
}

export function getFriendsRequestList(): Promise<UserProfile[]> {
  return apiGet<UserProfile[]>("/api/friends/friend_requests_list");
}

export interface MessageResponse {
  message: string;
}

export function sendFriendsRequest(id: string): Promise<MessageResponse> {
  return apiPostLink<MessageResponse>(`/api/friends/send_friend_request/${encodeURIComponent(id)}`);
}

export function acceptFriendRequest(id: string): Promise<MessageResponse> {
  return apiPostLink<MessageResponse>(`/api/friends/accept_friend_request/${encodeURIComponent(id)}`);
}

export function removeFriend(id: string): Promise<MessageResponse> {
  return apiDelete<MessageResponse>(`/api/friends/remove_friend/${encodeURIComponent(id)}`);
}

export function refuseFriendRequest(id: string): Promise<MessageResponse> {
  return apiDelete<MessageResponse>(`/api/friends/refuse_friend_request/${encodeURIComponent(id)}`);
}

export function receiveFriendRequest(id: string): void {
   const toastId = toast.add({
    title: "Friend request",
    description: `${id} has sent you a friend request`,
    actionProps: {
      children: "Accept",
      onClick() {
        acceptFriendRequest(id).catch((error: unknown) => {
          toast.add({
            type: "error",
            title: "Friend request",
            description: error instanceof Error ? error.message : String(error),
          });
        });
        toast.close(toastId)
      },
    },
  })
}