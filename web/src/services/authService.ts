import { apiGet, apiPost, apiPostForm, apiDelete, apiFetch } from "@/lib/api";
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

export function changeUsername(newUsername: string): Promise<UserPublic> {
  const encodedUsername = encodeURIComponent(newUsername);
  
  return apiPost<UserPublic>(`/api/user/change_username?new_username=${encodedUsername}`, null);
}

export function changePicture(file: File): Promise<UserPublic> {
  const formData = new FormData();
  formData.append("file", file); 

  return apiFetch<UserPublic>("/api/user/change_picture", {
    method: "POST",
    body: formData,
  });
}

export function deletePicture(): Promise<void> {
  return apiDelete<void>(`/api/user/remove_picture`);
}