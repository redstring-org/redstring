import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
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

afterEach(() => {
  vi.restoreAllMocks();
});

describe("CaseCard", () => {
  it("renders the locked visible sections", () => {
    render(<CaseCard activeCase={sampleCase} />);

    expect(screen.getByText("VendorCo contractor remote-access anomaly with potential on-campus linkage")).toBeTruthy();
    expect(screen.getByText("South Service Entrance SE-3 / Imaging Service Corridor")).toBeTruthy();
    expect(screen.getByText("Escalate Now")).toBeTruthy();
    expect(screen.getByText("John Mercer (VendorCo biomedical contractor)")).toBeTruthy();
    expect(screen.getByText("Trigger Summary")).toBeTruthy();
    expect(screen.getByText("Next Human Check")).toBeTruthy();
    expect(screen.getByText("Timeline")).toBeTruthy();
    expect(screen.getByText("Why Linked")).toBeTruthy();
    expect(screen.getByText("What Weakens It")).toBeTruthy();
    expect(screen.getByText("Provenance")).toBeTruthy();
    expect(screen.getByText("Escalation Recommendation")).toBeTruthy();
    expect(screen.getByText("Notify protective services leadership and SOC now.")).toBeTruthy();
  });
});

describe("App", () => {
  it("opens on the active case card without demo controls", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => sampleCase
      })
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("VendorCo contractor remote-access anomaly with potential on-campus linkage")).toBeTruthy();
    });

    expect(screen.queryByText("Demo Controls")).toBeNull();
    expect(screen.queryByText("Inject CY-0213-001")).toBeNull();
  });
});
