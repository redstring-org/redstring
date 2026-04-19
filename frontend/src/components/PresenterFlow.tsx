import { PRESENTER_STEPS } from "../demoContract";
import type { ActiveCase } from "../types";

type Props = {
  activeCase: ActiveCase;
  busy: boolean;
  onAdvance: () => Promise<void>;
  onReset: () => Promise<void>;
};

export function PresenterFlow({ activeCase, busy, onAdvance, onReset }: Props) {
  const done = PRESENTER_STEPS.filter((step) =>
    activeCase.timeline.some((item) => item.event_id === step.eventId)
  ).length;
  const next = PRESENTER_STEPS[done];

  return (
    <aside className="presenter-controls" aria-label="Presenter controls">
      <p className="presenter-note">
        Legacy presenter flow: manual demo-event injection only. The active case now opens from qualified live case groups.
      </p>
      <ol className="presenter-steps">
        {PRESENTER_STEPS.map((step, i) => {
          const status = i < done ? "complete" : i === done ? "ready" : "locked";
          return (
            <li key={step.id} className={`presenter-step presenter-step-${status}`}>
              <span className="presenter-step-label">{step.label}</span>
              <span className="presenter-step-state">{step.expectedState}</span>
            </li>
          );
        })}
      </ol>

      <div className="control-actions">
        <button
          className="btn-primary"
          disabled={busy || !next}
          onClick={onAdvance}
          type="button"
        >
          {busy ? "Loading…" : next ? `Advance → ${next.expectedState}` : "Complete"}
        </button>
        <button
          className="btn-ghost"
          disabled={busy || done === 0}
          onClick={onReset}
          type="button"
        >
          Reset
        </button>
      </div>
    </aside>
  );
}
