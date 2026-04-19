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
    fetchActiveCase()
      .then(setActiveCase)
      .catch((err: Error) => setError(err.message))
      .finally(() => setBusy(false));

    const applyLive = (r: LiveEventsResponse) => { setLiveEvents(r.events); setTotalEvents(r.total); };
    fetchLiveEvents().then(applyLive).catch(() => {});

    const interval = setInterval(() => {
      fetchLiveEvents().then(applyLive).catch(() => {});
    }, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
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
