import type { ActiveCase } from "../types";

type EventInjectionPanelProps = {
  activeCase: ActiveCase;
  busy: boolean;
  onInject: (eventId: string) => Promise<void>;
  onReset: () => Promise<void>;
};

export function EventInjectionPanel({
  activeCase,
  busy,
  onInject,
  onReset
}: EventInjectionPanelProps) {
  const cyberDisabled = busy || activeCase.state !== null;
  const badgeDisabled = busy || activeCase.state !== "Observe";
  const reportDisabled = busy || activeCase.state !== "Verify Now";
  const resetDisabled = busy || activeCase.timeline.length === 0;

  return (
    <aside className="control-panel">
      <div className="panel-eyebrow">Demo Controls</div>
      <p className="control-copy">
        Inject the locked gold-scenario events in order. The active case card remains the primary surface.
      </p>
      <div className="control-grid">
        <button disabled={cyberDisabled} onClick={() => onInject("CY-0213-001")} type="button">
          Inject CY-0213-001
        </button>
        <button disabled={badgeDisabled} onClick={() => onInject("AC-0224-001")} type="button">
          Inject AC-0224-001
        </button>
        <button disabled={reportDisabled} onClick={() => onInject("IR-0231-001")} type="button">
          Inject IR-0231-001
        </button>
        <button className="secondary" disabled={resetDisabled} onClick={onReset} type="button">
          Reset Demo
        </button>
      </div>
    </aside>
  );
}
