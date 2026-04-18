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

export async function injectEvent(eventId: string): Promise<ActiveCase> {
  const response = await fetch("/api/demo/inject", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ event_id: eventId })
  });
  return readJson<ActiveCase>(response);
}

export async function resetDemo(): Promise<ActiveCase> {
  const response = await fetch("/api/demo/reset", {
    method: "POST"
  });
  return readJson<ActiveCase>(response);
}
