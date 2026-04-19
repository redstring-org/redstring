import type { ActiveCase } from "./types";

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchActiveCase(): Promise<ActiveCase> {
  const response = await fetch("/api/case/active");
  return readJson<ActiveCase>(response);
}
