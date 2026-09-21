import { apiGet } from "@/lib/api";
import { type ChatDataProps } from "@/types/chat";

export function getChatHistory(): Promise<ChatDataProps[]> {
  return apiGet<ChatDataProps[]>("/api/chat/messages");
}
