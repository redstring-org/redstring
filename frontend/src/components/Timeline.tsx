import type { TimelineItem } from "../types";
import { EVENT_1, EVENT_2, EVENT_3 } from "../demoContract";

type Props = { items: TimelineItem[] };

type EventConfig = {
  time: string;
  text: string;
  source: string;
  pipClass: string;
  tagClass: string;
  abbr: string;
};

function config(item: TimelineItem): EventConfig {
  if (item.event_id === "CY-0213-001") {
    return { time: "02:13 AM", text: EVENT_1.replace(/^[\d:AP M—]+—\s*/, ""), source: "Cyber", pipClass: "pip-cyber", tagClass: "tag-cyber", abbr: "CY" };
  }
  if (item.event_id === "AC-0224-001") {
    return { time: "02:24 AM", text: EVENT_2.replace(/^[\d:AP M—]+—\s*/, ""), source: "Access Control", pipClass: "pip-access", tagClass: "tag-access", abbr: "AC" };
  }
  if (item.event_id === "IR-0231-001") {
    return { time: "02:31 AM", text: EVENT_3.replace(/^[\d:AP M—]+—\s*/, ""), source: "Officer Report", pipClass: "pip-officer", tagClass: "tag-officer", abbr: "IR" };
  }
  return {
    time: new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    text: item.summary,
    source: item.source,
    pipClass: "pip-default",
    tagClass: "",
    abbr: "??",
  };
}

export function Timeline({ items }: Props) {
  return (
    <div>
      <p className="eyebrow">Timeline</p>
      {items.length === 0 ? (
        <p className="placeholder">Awaiting the first qualified correlated case group.</p>
      ) : (
        <ol className="timeline-list">
          {items.map((item) => {
            const c = config(item);
            return (
              <li key={item.event_id} className="timeline-item">
                <div className="tl-icon">
                  <span className={`tl-pip ${c.pipClass}`}>{c.abbr}</span>
                </div>
                <div className="tl-body">
                  <div className="tl-time">{c.time}</div>
                  <div className="tl-text">{c.text}</div>
                  <span className={`tl-tag ${c.tagClass}`}>{c.source}</span>
                </div>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}
