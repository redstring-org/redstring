import type { ActiveCase } from "./types";

export const ACTIVE_CASE_ROUTE = "/case/active";
export const PENDING_CASE_TITLE = "Awaiting qualified correlated case group";
export const PENDING_TRIGGER_SUMMARY = "No case group has reached the minimum threshold of 3 linked events yet.";
export const PENDING_NEXT_ACTION = "Awaiting the first qualified case group from linked live events.";

export const CASE_TITLE = "VendorCo contractor remote-access anomaly with potential on-campus linkage";
export const CASE_LOCATION = "South Service Entrance SE-3 / Imaging Service Corridor";
export const CASE_PRIMARY_SUBJECT = "John Mercer (VendorCo biomedical contractor)";
export const CASE_TRIGGER_SUMMARY = "Successful VPN login from a new device while the remote session remains active.";

export const EVENT_1 =
  "02:13 AM — jmercer@vendorco successful VPN login from a new device while the remote session remains active.";
export const EVENT_2 = "02:24 AM — badge B-1842 used at South Service Entrance SE-3 after hours.";
export const EVENT_3 =
  "02:31 AM — officer report: male in VendorCo jacket moving two equipment cases toward Imaging Service Corridor; no escort observed.";

export const NEXT_CHECK_1 =
  "Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live and whether the MFA approval was legitimate.";
export const NEXT_CHECK_2 =
  "Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite and carrying badge B-1842.";
export const NEXT_CHECK_3 =
  "Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3.";

export const ESCALATION_RECOMMENDATION = "Notify protective services leadership and SOC now.";

export const EMPTY_ACTIVE_CASE: ActiveCase = {
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

export type PresenterStep = {
  id: string;
  eventId: string;
  label: string;
  eventSummary: string;
  expectedState: NonNullable<ActiveCase["state"]>;
  expectedNextAction: string;
};

export const PRESENTER_STEPS: PresenterStep[] = [
  {
    id: "step-1",
    eventId: "CY-0213-001",
    label: "Step 1",
    eventSummary: EVENT_1,
    expectedState: "Observe",
    expectedNextAction: NEXT_CHECK_1
  },
  {
    id: "step-2",
    eventId: "AC-0224-001",
    label: "Step 2",
    eventSummary: EVENT_2,
    expectedState: "Verify Now",
    expectedNextAction: NEXT_CHECK_2
  },
  {
    id: "step-3",
    eventId: "IR-0231-001",
    label: "Step 3",
    eventSummary: EVENT_3,
    expectedState: "Escalate Now",
    expectedNextAction: NEXT_CHECK_3
  }
];
