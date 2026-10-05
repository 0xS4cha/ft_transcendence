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

export function downloadJson(data: unknown[], filename: string) {
  const blob = new Blob(
    [JSON.stringify(data, null, 2)],
    { type: "application/json" }
  );

  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();

  URL.revokeObjectURL(url);
}