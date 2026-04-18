from fastapi import APIRouter, Request, HTTPException

from app.correlation.engine import build_basic_alert, find_all_cross_domain_clusters
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[Alert])
def list_alerts(request: Request) -> list[Alert]:
    return request.app.state.store.list_alerts()


@router.post("/refresh", response_model=list[Alert])
def refresh_alerts(request: Request) -> list[Alert]:
    store = request.app.state.store
    events = store.list_events()

    clusters = find_all_cross_domain_clusters(events)
    alerts = [build_basic_alert(c) for c in clusters if build_basic_alert(c)]

    seen = set()
    unique_alerts = []

    for alert in alerts:
        key = (alert.facility_id, tuple(sorted(alert.event_ids)))
        if key not in seen:
            seen.add(key)
            unique_alerts.append(alert)

    return store.replace_alerts(unique_alerts)


@router.get("/check")
def check_alerts(request: Request) -> dict:
    events = request.app.state.store.list_events()
    cluster = find_first_cross_domain_cluster(events)
    alert = build_basic_alert(cluster)

    return {
        "has_correlation": len(cluster) > 0,
        "alert": alert.model_dump() if alert else None,
        "matched_events": [event.model_dump() for event in cluster],
    }

@router.get("/{alert_id}/events")
def get_alert_events(alert_id: str, request: Request):
    store = request.app.state.store
    alert = store.get_alert(alert_id)

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    events = store.list_events()
    matched = [e for e in events if e.id in alert.event_ids]

    return [e.model_dump() for e in matched]