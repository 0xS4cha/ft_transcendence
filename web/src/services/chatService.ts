import { apiGet, apiPost } from "@/lib/api";
import { type ChatDataProps } from "@/types/chat";

export function getChatHistory(): Promise<ChatDataProps[]> {
  return apiGet<ChatDataProps[]>("/api/chat/messages");
}

export function sendChatMessage(message: string): Promise<undefined> {
  return apiPost<undefined>("/api/chat/send", message);
}