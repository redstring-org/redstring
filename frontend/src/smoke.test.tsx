import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { CaseCard } from "./components/CaseCard";
import {
  ACTIVE_CASE_ROUTE,
  CASE_LOCATION,
  CASE_PRIMARY_SUBJECT,
  CASE_TITLE,
  CASE_TRIGGER_SUMMARY,
  ESCALATION_RECOMMENDATION,
  EVENT_1,
  NEXT_CHECK_3,
  PENDING_CASE_TITLE,
  PENDING_NEXT_ACTION,
  PENDING_TRIGGER_SUMMARY,
} from "./demoContract";
import type { ActiveCase, LiveEventsResponse } from "./types";

const mockContext2D = {
  clearRect: vi.fn(),
  createLinearGradient: vi.fn(() => ({ addColorStop: vi.fn() })),
  beginPath: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  stroke: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  strokeStyle: "",
  lineWidth: 1,
  fillStyle: "",
};

HTMLCanvasElement.prototype.getContext = vi.fn(() => mockContext2D as unknown as CanvasRenderingContext2D);

const emptyCase: ActiveCase = {
  case_id: "CASE-GROUP-PENDING",
  case_title: PENDING_CASE_TITLE,
  location: "",
  state: null,
  primary_subject: "Unknown subject",
  trigger_summary: PENDING_TRIGGER_SUMMARY,
  timeline: [],
  why_linked: [],
  what_weakens_it: [],
  next_human_check: "",
  escalation_recommendation: null,
  provenance: [],
  osint_enabled: false
};

const sampleCase: ActiveCase = {
  case_id: "CASE-GOLD-001",
  case_title: CASE_TITLE,
  location: CASE_LOCATION,
  state: "Escalate Now",
  primary_subject: CASE_PRIMARY_SUBJECT,
  trigger_summary: CASE_TRIGGER_SUMMARY,
  timeline: [
    {
      event_id: "CY-0213-001",
      timestamp: "2026-04-18T02:13:00-04:00",
      summary: EVENT_1,
      source: "identity_risk_engine"
    }
  ],
  why_linked: ["Unexpected device login succeeded on vendor contractor account"],
  what_weakens_it: ["Contractor schedule not yet confirmed"],
  next_human_check: NEXT_CHECK_3,
  escalation_recommendation: ESCALATION_RECOMMENDATION,
  provenance: [
    {
      event_id: "CY-0213-001",
      label: "Cyber trigger",
      source: "identity_risk_engine",
      timestamp: "2026-04-18T02:13:00-04:00"
    }
  ],
  osint_enabled: false
};

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe("CaseCard", () => {
  it("renders the active case sections", () => {
    render(<CaseCard activeCase={sampleCase} />);

    expect(screen.getByText("South Service Entrance SE-3 / Imaging Service Corridor")).toBeTruthy();
    expect(screen.getByText("Escalate Now")).toBeTruthy();
    expect(screen.getByText("John Mercer (VendorCo biomedical contractor)")).toBeTruthy();
    expect(screen.getByText("Trigger")).toBeTruthy();
    expect(screen.getByText("Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.")).toBeTruthy();
    expect(screen.getByText("Timeline")).toBeTruthy();
    expect(screen.getByText("Why Linked")).toBeTruthy();
    expect(screen.getByText("What Weakens It")).toBeTruthy();
    expect(screen.getByText("Provenance")).toBeTruthy();
    expect(screen.getByText("Escalation Recommendation")).toBeTruthy();
    expect(screen.getByText("Notify protective services leadership and SOC now.")).toBeTruthy();
  });

  it("renders the qualified-group pending copy when no case is active yet", () => {
    render(<CaseCard activeCase={emptyCase} />);

    expect(screen.getByText("Awaiting Case Group")).toBeTruthy();
    expect(screen.getByText(PENDING_NEXT_ACTION)).toBeTruthy();
    expect(screen.getByText(PENDING_TRIGGER_SUMMARY)).toBeTruthy();
    expect(screen.getByText("Awaiting the first qualified correlated case group.")).toBeTruthy();
  });
});

describe("App", () => {
  it("opens on the active case card without demo controls", async () => {
    const fetchMock = vi.fn(async (input: string | URL | Request) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.pathname : input.url;
      if (url.endsWith("/api/case/active")) {
        return { ok: true, json: async () => sampleCase };
      }
      return { ok: true, json: async () => ({ total: 0, events: [] } satisfies LiveEventsResponse) };
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.")).toBeTruthy();
      expect(screen.getByText("South Service Entrance SE-3 / Imaging Service Corridor")).toBeTruthy();
    });

    expect(screen.queryByText("Demo Controls")).toBeNull();
    expect(screen.queryByText("Inject CY-0213-001")).toBeNull();
  });

  it("refreshes the active case when polling discovers a newly qualified case group", async () => {
    let activeCaseCalls = 0;
    const fetchMock = vi.fn(async (input: string | URL | Request) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.pathname : input.url;
      if (url.endsWith("/api/case/active")) {
        activeCaseCalls += 1;
        return {
          ok: true,
          json: async () => (activeCaseCalls === 1 ? emptyCase : sampleCase),
        };
      }
      return { ok: true, json: async () => ({ total: 1, events: [] } satisfies LiveEventsResponse) };
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    await screen.findByText(PENDING_NEXT_ACTION);

    await waitFor(() => {
      expect(screen.getByText("Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.")).toBeTruthy();
    }, { timeout: 7000 });
    expect(screen.getByText("South Service Entrance SE-3 / Imaging Service Corridor")).toBeTruthy();
  }, 8000);
});
