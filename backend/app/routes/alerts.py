from fastapi import APIRouter, Request

from app.correlation.engine import has_cross_domain_correlation

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/check")
def check_alerts(request: Request) -> dict[str, bool]:
    events = request.app.state.store.list_events()
    return {"has_correlation": has_cross_domain_correlation(events)}