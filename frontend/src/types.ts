export type TimelineItem = {
  event_id: string;
  timestamp: string;
  summary: string;
  source: string;
};

export type ProvenanceItem = {
  event_id: string;
  label: string;
  source: string;
  timestamp: string;
};

export type ActiveCase = {
  case_id: string;
  case_title: string;
  location: string;
  state: "Observe" | "Verify Now" | "Escalate Now" | null;
  primary_subject: string;
  trigger_summary: string;
  timeline: TimelineItem[];
  why_linked: string[];
  what_weakens_it: string[];
  next_human_check: string;
  escalation_recommendation: string | null;
  provenance: ProvenanceItem[];
  osint_enabled: boolean;
};
