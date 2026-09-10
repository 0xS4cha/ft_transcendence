import { apiGet, apiPost, apiPostForm } from "@/lib/api";
import { type SignupPayload, type UserPublic } from "@/types/user";

export function login(email: string, password: string): Promise<UserPublic> {
  const body = new URLSearchParams({
    username: email,
    password,
  });
  return apiPostForm<UserPublic>("/api/auth/login/token", body);
}

export function signup(data: SignupPayload): Promise<UserPublic> {
  return apiPost<UserPublic>("/api/auth/signup/signup", data);
}

export function getCurrentUser(): Promise<UserPublic> {
  return apiGet<UserPublic>("/api/auth/login/users/me");
}

export function logout(): Promise<void> {
  return apiPost<void>("/api/auth/logout/logout", {});
}
