import { apiGet, apiPost } from "@/lib/api";
import { type ChatDataProps } from "@/types/chat";

export function getChatHistory(): Promise<ChatDataProps[]> {
  return apiGet<ChatDataProps[]>("/api/chat/messages");
}

export function sendChatMessage(content: string): Promise<ChatDataProps> {
  return apiPost<ChatDataProps>("/api/chat/send", { content: content });
}