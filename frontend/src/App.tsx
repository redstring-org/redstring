import { useEffect, useState } from "react";
import { fetchActiveCase, fetchLiveEvents, injectEvent, resetDemo } from "./api";
import { CaseCard } from "./components/CaseCard";
import { LiveFeed } from "./components/LiveFeed";
import { PresenterFlow } from "./components/PresenterFlow";
import { RedStringCanvas } from "./components/RedStringCanvas";
import { ACTIVE_CASE_ROUTE, EMPTY_ACTIVE_CASE, PRESENTER_STEPS } from "./demoContract";
import type { ActiveCase, LiveEvent, LiveEventsResponse } from "./types";

const POLL_INTERVAL_MS = 3000;

export default function App() {
  const [activeCase, setActiveCase] = useState<ActiveCase>(EMPTY_ACTIVE_CASE);
  const [liveEvents, setLiveEvents] = useState<LiveEvent[]>([]);
  const [totalEvents, setTotalEvents] = useState(0);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [routeReady, setRouteReady] = useState(false);

  useEffect(() => {
    if (window.location.pathname !== ACTIVE_CASE_ROUTE) {
      window.history.replaceState({}, "", ACTIVE_CASE_ROUTE);
    }
    setRouteReady(true);
  }, []);

  useEffect(() => {
    if (!routeReady) return;
    let cancelled = false;
    const applyLive = (r: LiveEventsResponse) => {
      if (cancelled) return;
      setLiveEvents(r.events);
      setTotalEvents(r.total);
    };
    const syncActiveCase = async (showBusy: boolean) => {
      if (showBusy) setBusy(true);
      try {
        const active = await fetchActiveCase();
        if (!cancelled) {
          setActiveCase(active);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) setError((err as Error).message);
      } finally {
        if (showBusy && !cancelled) setBusy(false);
      }
    };
    const syncLiveEvents = async () => {
      try {
        applyLive(await fetchLiveEvents());
      } catch {
        // Keep the existing feed visible if a poll fails.
      }
    };
    const sync = async (showBusy: boolean) => {
      await Promise.all([syncActiveCase(showBusy), syncLiveEvents()]);
    };

    void sync(true);

    const interval = setInterval(() => {
      void sync(false);
    }, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [routeReady]);

  async function handleInject(eventId: string) {
    setBusy(true);
    setError(null);
    try {
      setActiveCase(await injectEvent(eventId));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function handleReset() {
    setBusy(true);
    setError(null);
    try {
      setActiveCase(await resetDemo());
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function handleAdvance() {
    const next = PRESENTER_STEPS[activeCase.timeline.length];
    if (next) await handleInject(next.eventId);
  }

  if (!routeReady) return null;

  return (
    <main className="app-shell">
      <RedStringCanvas />
      <header className="app-header">
        <span className="app-wordmark">RedString</span>
        <span className="app-live-badge">Live Case</span>
      </header>
      <div className="app-body">
        <section className="stage">
          <CaseCard activeCase={activeCase} />
          <PresenterFlow
            activeCase={activeCase}
            busy={busy}
            onAdvance={handleAdvance}
            onReset={handleReset}
          />
        </section>
        <LiveFeed events={liveEvents} total={totalEvents} />
      </div>
      {error && <p className="error-banner">{error}</p>}
    </main>
  );
}
