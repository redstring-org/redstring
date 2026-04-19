import type { ActiveCase } from "../types";
import { EvidenceList } from "./EvidenceList";
import { Timeline } from "./Timeline";

type Props = { activeCase: ActiveCase };

function stateClass(state: ActiveCase["state"]) {
  if (state === "Observe")      return "state-observe";
  if (state === "Verify Now")   return "state-verify";
  if (state === "Escalate Now") return "state-escalate";
  return "state-pending";
}

export function CaseCard({ activeCase }: Props) {
  const sc = stateClass(activeCase.state);
  const hasAction = Boolean(activeCase.next_human_check);

  return (
    <article className={`case-card ${sc}`}>

      {/* 1 — State badge (most prominent) + next action */}
      <div className="state-hero">
        <span className="state-badge">
          <span className="badge-dot" />
          {activeCase.state ?? "Awaiting Trigger"}
        </span>
        <p className={`next-action-text${hasAction ? "" : " idle"}`}>
          {activeCase.next_human_check ||
            "Awaiting qualifying cyber trigger from SOC or identity tooling."}
        </p>
      </div>

      {/* 2 — Case metadata (subordinate strip) */}
      <dl className="case-meta">
        <div className="meta-field">
          <dt className="meta-label">Subject</dt>
          <dd className="meta-value">{activeCase.primary_subject}</dd>
        </div>
        <div className="meta-field">
          <dt className="meta-label">Location</dt>
          <dd className="meta-value">{activeCase.location}</dd>
        </div>
        <div className="meta-field meta-field-full">
          <dt className="meta-label">Trigger</dt>
          <dd className="meta-value">{activeCase.trigger_summary}</dd>
        </div>
      </dl>

      {/* 3 — Evidence panels */}
      <div className="evidence-grid">
        <Timeline items={activeCase.timeline} />
        <div className="evidence-col">
          <EvidenceList
            title="Why Linked"
            items={activeCase.why_linked}
            emptyText="No linked evidence yet."
            tone="linked"
          />
          <EvidenceList
            title="What Weakens It"
            items={activeCase.what_weakens_it}
            emptyText="Weakening factors appear as the case develops."
            tone="weaken"
          />
        </div>
      </div>

      {/* 4 — Escalation (only at Escalate Now) */}
      {activeCase.escalation_recommendation && (
        <div className="escalation-bar">
          <div className="esc-icon">⚠</div>
          <div>
            <p className="esc-label">Escalation Recommendation</p>
            <p className="esc-message">{activeCase.escalation_recommendation}</p>
          </div>
        </div>
      )}

      {/* 5 — Provenance */}
      <div className="provenance-bar">
        <span className="prov-label">Provenance</span>
        {activeCase.provenance.length === 0 ? (
          <span className="prov-empty">Will appear as events are injected.</span>
        ) : (
          activeCase.provenance.map((item) => (
            <span className="prov-chip" key={item.event_id}>
              <strong>{item.label}</strong>
              <span className="prov-sep">·</span>
              <span>{item.source}</span>
              <span className="prov-sep">·</span>
              <span>
                {new Date(item.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </span>
          ))
        )}
      </div>

    </article>
  );
}
