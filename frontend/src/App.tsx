import { useEffect, useState } from "react";
import { fetchActiveCase } from "./api";
import { CaseCard } from "./components/CaseCard";
import type { ActiveCase } from "./types";

export const emptyCase: ActiveCase = {
  case_id: "CASE-GOLD-001",
  case_title: "VendorCo contractor remote-access anomaly with potential on-campus linkage",
  location: "South Service Entrance SE-3 / Imaging Service Corridor",
  state: null,
  primary_subject: "John Mercer (VendorCo biomedical contractor)",
  trigger_summary: "Successful VPN login from a new device while the remote session remains active.",
  timeline: [],
  why_linked: [],
  what_weakens_it: [],
  next_human_check: "",
  escalation_recommendation: null,
  provenance: [],
  osint_enabled: false
};

export default function App() {
  const [activeCase, setActiveCase] = useState<ActiveCase>(emptyCase);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchActiveCase().then(setActiveCase).catch((requestError: Error) => setError(requestError.message));
  }, []);

  return (
    <main className="app-shell">
      <section className="stage">
        <CaseCard activeCase={activeCase} />
      </section>
      {error ? <p className="error-banner">{error}</p> : null}
    </main>
  );
}
