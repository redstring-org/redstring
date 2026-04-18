from fastapi import FastAPI

from app.routes.alerts import router as alerts_router
from app.routes.events import router as events_router
from app.routes.simulate import router as simulate_router
from app.store.memory import MemoryStore

app = FastAPI(title="Critical Ops API")
app.state.store = MemoryStore()

app.include_router(events_router)
app.include_router(simulate_router)
app.include_router(alerts_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}