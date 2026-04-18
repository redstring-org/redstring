from fastapi import FastAPI

from app.routes.events import router as events_router
from app.store.memory import MemoryStore

app = FastAPI(title="RedString API")
app.state.store = MemoryStore()

app.include_router(events_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}