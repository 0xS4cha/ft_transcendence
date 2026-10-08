import { apiGet, apiPost, apiPostForm, apiDelete } from "@/lib/api";
import { type SignupPayload, type UserPublic } from "@/types/user";

export function login(email: string, password: string): Promise<UserPublic> {
  const body = new URLSearchParams({
    username: email,
    password,
  });
  return apiPostForm<UserPublic>("/api/auth/login", body);
}

export function signup(data: SignupPayload): Promise<UserPublic> {
  return apiPost<UserPublic>("/api/auth/signup", data);
}

export function getCurrentUser(): Promise<UserPublic> {
  return apiGet<UserPublic>("/api/auth/me");
}

export function logout(): Promise<void> {
  return apiPost<void>("/api/auth/logout", {});
}

export function delete_rgpd(): Promise<void> {
  return apiDelete<void>("/api/auth/me");
}

export function setUsername(test: string): Promise<void> {
  return apiPost<void>("/api/", test)
}