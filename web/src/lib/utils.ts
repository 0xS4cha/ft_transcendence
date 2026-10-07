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

export function downloadXml(data: unknown[], filename: string) {
  const arrayToXml = (arr: unknown[], rootName: string): string => {
    const items = arr.map((item) => {
      if (typeof item !== 'object' || item === null) {
        return `<item>${item}</item>`;
      }
      const obj = item as Record<string, unknown>;
      const fields = Object.entries(obj)
        .map(([key, value]) => {
          if (Array.isArray(value)) {
            const items = value.map(v => `<item>${v}</item>`).join('');
            return `<${key}>${items}</${key}>`;
          }
          return `<${key}>${value}</${key}>`;
        })
        .join('');
      return `<row>${fields}</row>`;
    });
    return `<?xml version="1.0" encoding="UTF-8"?><${rootName}>${items.join('')}</${rootName}>`;
  };

  const xmlContent = arrayToXml(data, 'data');
  const blob = new Blob([xmlContent], { type: 'application/xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}