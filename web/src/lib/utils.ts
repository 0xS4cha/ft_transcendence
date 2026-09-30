import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function initialsOf(username: string) {
  if (!username) return "";
  return username.slice(0, 2).toUpperCase();
}

export function errorMessage(error: unknown) {
  return error instanceof Error ? error.message : String(error);
}