import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { CaseCard } from "./components/CaseCard";
import { PresenterFlow } from "./components/PresenterFlow";
import {
  ACTIVE_CASE_ROUTE,
  CASE_LOCATION,
  CASE_PRIMARY_SUBJECT,
  CASE_TITLE,
  CASE_TRIGGER_SUMMARY,
  ESCALATION_RECOMMENDATION,
  EVENT_1,
  EVENT_2,
  EVENT_3,
  NEXT_CHECK_1,
  NEXT_CHECK_2,
  NEXT_CHECK_3
} from "./demoContract";
import type { ActiveCase } from "./types";

const emptyCase: ActiveCase = {
  case_id: "CASE-GOLD-001",
  case_title: CASE_TITLE,
  location: CASE_LOCATION,
  state: null,
  primary_subject: CASE_PRIMARY_SUBJECT,
  trigger_summary: CASE_TRIGGER_SUMMARY,
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

const observeCase: ActiveCase = {
  ...emptyCase,
  state: "Observe",
  next_human_check: NEXT_CHECK_1,
  timeline: [
    {
      event_id: "CY-0213-001",
      timestamp: "2026-04-18T02:13:00-04:00",
      summary: EVENT_1,
      source: "identity_risk_engine"
    }
  ],
  why_linked: [
    "Unexpected device login succeeded on vendor contractor account",
    "Active VPN session remains live"
  ],
  what_weakens_it: [
    "No linked on-campus evidence yet",
    "Remote session legitimacy not yet confirmed"
  ],
  provenance: [
    {
      event_id: "CY-0213-001",
      label: "Cyber trigger",
      source: "identity_risk_engine",
      timestamp: "2026-04-18T02:13:00-04:00"
    }
  ]
};

const verifyCase: ActiveCase = {
  ...observeCase,
  state: "Verify Now",
  next_human_check: NEXT_CHECK_2,
  timeline: [
    ...observeCase.timeline,
    {
      event_id: "AC-0224-001",
      timestamp: "2026-04-18T02:24:00-04:00",
      summary: EVENT_2,
      source: "badge_access_control"
    }
  ],
  why_linked: [
    ...observeCase.why_linked,
    "Badge B-1842 maps to John Mercer",
    "After-hours badge use at South Service Entrance SE-3"
  ],
  what_weakens_it: [
    "Contractor schedule not yet confirmed",
    "Remote session legitimacy not yet confirmed"
  ],
  provenance: [
    ...observeCase.provenance,
    {
      event_id: "AC-0224-001",
      label: "Badge/access event",
      source: "badge_access_control",
      timestamp: "2026-04-18T02:24:00-04:00"
    }
  ]
};

const escalateCase: ActiveCase = {
  ...verifyCase,
  state: "Escalate Now",
  next_human_check: NEXT_CHECK_3,
  timeline: [
    ...verifyCase.timeline,
    {
      event_id: "IR-0231-001",
      timestamp: "2026-04-18T02:31:00-04:00",
      summary: EVENT_3,
      source: "officer_radio_report"
    }
  ],
  why_linked: [
    ...verifyCase.why_linked,
    "Officer report in adjacent Imaging Service Corridor within seven minutes",
    "No escort observed"
  ],
  escalation_recommendation: ESCALATION_RECOMMENDATION,
  provenance: [
    ...verifyCase.provenance,
    {
      event_id: "IR-0231-001",
      label: "Suspicious-person report",
      source: "officer_radio_report",
      timestamp: "2026-04-18T02:31:00-04:00"
    }
  ]
};

function jsonResponse(body: unknown) {
  return Promise.resolve(
    new Response(JSON.stringify(body), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    })
  );
}

beforeEach(() => {
  window.history.replaceState({}, "", "/");
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("CaseCard", () => {
  it("renders the primary case content", () => {
    render(<CaseCard activeCase={sampleCase} />);
    expect(screen.getByText(CASE_TITLE)).toBeTruthy();
    expect(screen.getByText("Escalate Now")).toBeTruthy();
    expect(screen.getByText("Notify protective services leadership and SOC now.")).toBeTruthy();
    expect(screen.getByText(CASE_PRIMARY_SUBJECT)).toBeTruthy();
    expect(screen.getByText(EVENT_1)).toBeTruthy();
  });
});

describe("PresenterFlow", () => {
  it("renders the locked three-step flow", () => {
    render(<PresenterFlow activeCase={sampleCase} busy={false} onAdvance={async () => undefined} onReset={async () => undefined} />);
    expect(screen.getByText("Step 1")).toBeTruthy();
    expect(screen.getByText("Step 2")).toBeTruthy();
    expect(screen.getByText("Step 3")).toBeTruthy();
    expect(screen.getByText("Advance scenario")).toBeTruthy();
    expect(screen.getByText("Reset demo")).toBeTruthy();
  });
});

describe("App demo flow", () => {
  it("hydrates, advances through the locked sequence, and resets the same active case", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = typeof input === "string" ? input : input.toString();

      if (url === "/api/case/active") {
        return jsonResponse(emptyCase);
      }

      if (url === "/api/demo/inject") {
        const payload = JSON.parse(String(init?.body ?? "{}")) as { event_id?: string };
        if (payload.event_id === "CY-0213-001") {
          return jsonResponse(observeCase);
        }
        if (payload.event_id === "AC-0224-001") {
          return jsonResponse(verifyCase);
        }
        if (payload.event_id === "IR-0231-001") {
          return jsonResponse(escalateCase);
        }
      }

      if (url === "/api/demo/reset") {
        return jsonResponse(emptyCase);
      }

      throw new Error(`Unexpected request: ${url}`);
    });

    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    await screen.findByText("Awaiting Trigger");
    await waitFor(() => {
      expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/case/active");
    });
    expect(window.location.pathname).toBe(ACTIVE_CASE_ROUTE);
    expect(screen.getByText("Awaiting Trigger")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "Advance scenario" }));

    await screen.findByText("Observe");
    expect(screen.getByText(NEXT_CHECK_1)).toBeTruthy();
    expect(fetchMock.mock.calls[1]?.[0]).toBe("/api/demo/inject");
    expect(fetchMock.mock.calls[1]?.[1]).toMatchObject({
      method: "POST",
      body: JSON.stringify({ event_id: "CY-0213-001" })
    });

    fireEvent.click(screen.getByRole("button", { name: "Advance scenario" }));

    await screen.findByText("Verify Now");
    expect(screen.getByText(NEXT_CHECK_2)).toBeTruthy();
    expect(fetchMock.mock.calls[2]?.[1]).toMatchObject({
      method: "POST",
      body: JSON.stringify({ event_id: "AC-0224-001" })
    });

    fireEvent.click(screen.getByRole("button", { name: "Advance scenario" }));

    await screen.findByText("Escalate Now");
    expect(screen.getByText(NEXT_CHECK_3)).toBeTruthy();
    expect(screen.getByText(ESCALATION_RECOMMENDATION)).toBeTruthy();
    expect(fetchMock.mock.calls[3]?.[1]).toMatchObject({
      method: "POST",
      body: JSON.stringify({ event_id: "IR-0231-001" })
    });

    fireEvent.click(screen.getByRole("button", { name: "Reset demo" }));

    await screen.findByText("Awaiting Trigger");
    expect(fetchMock.mock.calls[4]?.[0]).toBe("/api/demo/reset");
    expect(fetchMock.mock.calls[4]?.[1]).toMatchObject({ method: "POST" });
  });
});
