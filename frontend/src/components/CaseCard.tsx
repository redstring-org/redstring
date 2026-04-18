import type { ActiveCase } from "../types";
import { EvidenceList } from "./EvidenceList";
import { Timeline } from "./Timeline";

type CaseCardProps = {
  activeCase: ActiveCase;
};

export function CaseCard({ activeCase }: CaseCardProps) {
  return (
    <article className="case-card">
      <header className="case-header">
        <div>
          <p className="kicker">Hospital Security Duty Manager</p>
          <h1>{activeCase.case_title}</h1>
          <p className="subhead">{activeCase.location}</p>
        </div>
        <div className="state-stack">
          <span className={`state-badge ${activeCase.state ? "state-live" : "state-empty"}`}>
            {activeCase.state ?? "State Pending"}
          </span>
          <span className="subject-chip">{activeCase.primary_subject}</span>
        </div>
      </header>

      <section className="hero-panel">
        <div>
          <div className="panel-eyebrow">Trigger Summary</div>
          <p className="hero-copy">{activeCase.trigger_summary}</p>
        </div>
        <div>
          <div className="panel-eyebrow">Next Human Check</div>
          <p className="next-action">
            {activeCase.next_human_check || "Awaiting the qualifying cyber trigger before a deterministic action is shown."}
          </p>
        </div>
      </section>

      <div className="panel-grid">
        <Timeline items={activeCase.timeline} />
        <EvidenceList
          title="Why Linked"
          items={activeCase.why_linked}
          emptyText="No linked evidence yet."
        />
        <EvidenceList
          title="What Weakens It"
          items={activeCase.what_weakens_it}
          emptyText="Weakening factors will appear once the case opens."
        />
        <section className="panel">
          <div className="panel-eyebrow">Provenance</div>
          {activeCase.provenance.length === 0 ? (
            <p className="placeholder">Visible evidence provenance will appear as events are injected.</p>
          ) : (
            <ul className="provenance-list">
              {activeCase.provenance.map((item) => (
                <li key={item.event_id}>
                  <strong>{item.label}</strong>
                  <span>{item.source}</span>
                  <span>{new Date(item.timestamp).toLocaleString()}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      {activeCase.escalation_recommendation ? (
        <section className="escalation-banner">
          <div className="panel-eyebrow">Escalation Recommendation</div>
          <p>{activeCase.escalation_recommendation}</p>
        </section>
      ) : null}
    </article>
  );
}
