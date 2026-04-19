import type { ActiveCase, LiveEventsResponse } from "./types";

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchActiveCase(): Promise<ActiveCase> {
  return readJson<ActiveCase>(await fetch("/api/case/active"));
}

export async function injectEvent(eventId: string): Promise<ActiveCase> {
  return readJson<ActiveCase>(
    await fetch("/api/demo/inject", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event_id: eventId }),
    })
  );
}

export async function resetDemo(): Promise<ActiveCase> {
  return readJson<ActiveCase>(await fetch("/api/demo/reset", { method: "POST" }));
}

export async function fetchLiveEvents(): Promise<LiveEventsResponse> {
  return readJson<LiveEventsResponse>(await fetch("/api/events/live"));
}
