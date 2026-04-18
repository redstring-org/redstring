import type { TimelineItem } from "../types";

type TimelineProps = {
  items: TimelineItem[];
};

export function Timeline({ items }: TimelineProps) {
  return (
    <section className="panel">
      <div className="panel-eyebrow">Timeline</div>
      {items.length === 0 ? (
        <p className="placeholder">Awaiting the qualifying cyber trigger.</p>
      ) : (
        <ol className="timeline-list">
          {items.map((item) => (
            <li key={item.event_id} className="timeline-item">
              <div className="timeline-summary">{item.summary}</div>
              <div className="timeline-meta">
                <span>{item.source}</span>
                <span>{new Date(item.timestamp).toLocaleString()}</span>
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
