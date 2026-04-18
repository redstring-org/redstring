import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { CaseCard } from "./components/CaseCard";
import type { ActiveCase } from "./types";

const sampleCase: ActiveCase = {
  case_id: "CASE-GOLD-001",
  case_title: "VendorCo contractor remote-access anomaly with potential on-campus linkage",
  location: "South Service Entrance SE-3 / Imaging Service Corridor",
  state: "Escalate Now",
  primary_subject: "John Mercer (VendorCo biomedical contractor)",
  trigger_summary: "Successful VPN login from a new device while the remote session remains active.",
  timeline: [
    {
      event_id: "CY-0213-001",
      timestamp: "2026-04-18T02:13:00-04:00",
      summary: "02:13 AM - jmercer@vendorco successful VPN login from a new device while the remote session remains active.",
      source: "identity_risk_engine"
    }
  ],
  why_linked: ["Unexpected device login succeeded on vendor contractor account"],
  what_weakens_it: ["Contractor schedule not yet confirmed"],
  next_human_check: "Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.",
  escalation_recommendation: "Notify protective services leadership and SOC now.",
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

describe("CaseCard", () => {
  it("renders the primary case content", () => {
    render(<CaseCard activeCase={sampleCase} />);
    expect(screen.getByText("Escalate Now")).toBeTruthy();
    expect(screen.getByText("Notify protective services leadership and SOC now.")).toBeTruthy();
    expect(screen.getByText("John Mercer (VendorCo biomedical contractor)")).toBeTruthy();
  });
});
