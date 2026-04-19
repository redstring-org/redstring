import { useEffect, useRef, useState } from "react";
import type { LiveEvent } from "../types";

type Props = { events: LiveEvent[]; total: number };

const KIND_META: Record<string, { label: string; cls: string }> = {
  badge_access:             { label: "Badge",  cls: "feed-tag-badge"   },
  suspicious_person_report: { label: "Report", cls: "feed-tag-report"  },
  osint_post:               { label: "OSINT",  cls: "feed-tag-osint"   },
};

function formatTime(ts: string | null): string {
  if (!ts) return "--:--:--";
  try {
    return new Date(ts).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return "--:--:--";
  }
}

export function LiveFeed({ events, total }: Props) {
  const [newIds, setNewIds] = useState<Set<number>>(new Set());
  const prevCountRef = useRef(0);

  useEffect(() => {
    if (events.length > prevCountRef.current) {
      const added = events.slice(prevCountRef.current).map((e) => e.id);
      setNewIds(new Set(added));
      const timer = setTimeout(() => setNewIds(new Set()), 1400);
      prevCountRef.current = events.length;
      return () => clearTimeout(timer);
    }
    prevCountRef.current = events.length;
  }, [events]);

  const reversed = [...events].reverse();

  return (
    <section className="live-feed">
      <div className="live-feed-header">
        <span className="live-feed-title">
          <span className="live-feed-dot" />
          Live Event Feed
        </span>
        <span className="live-feed-count">{total} events processed</span>
      </div>

      <div className="live-feed-scroll">
        {reversed.length === 0 ? (
          <p className="feed-empty">
            No events yet. Stream data to see the noise RedString is processing:
            <code>python data_gen/post_badge_events_csv.py --interval-seconds 0.5</code>
          </p>
        ) : (
          reversed.map((ev) => {
            const meta = KIND_META[ev.kind] ?? { label: ev.kind, cls: "feed-tag-default" };
            return (
              <div
                key={ev.id}
                className={`feed-row${newIds.has(ev.id) ? " feed-row-new" : ""}`}
              >
                <span className="feed-time">{formatTime(ev.timestamp)}</span>
                <span className={`feed-tag ${meta.cls}`}>{meta.label}</span>
                <span className="feed-summary">{ev.summary}</span>
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}
