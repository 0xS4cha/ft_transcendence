import { type ChatDataProps } from "@/types/chat";

export interface UserPublic {
  id: number;
  email: string;
  username: string;
  picture?: string;
  chat?: ChatDataProps[];
  isDark?: boolean;
}

export interface FriendState extends UserPublic {
  online: boolean;
}

export interface UserState extends UserPublic {
  isAuthenticated: boolean;
  status: "idle" | "loading" | "ready";
}

export interface SignupPayload {
  email: string;
  password: string;
  confirm_password: string;
}
