from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.state_store import store


client = TestClient(app)


def setup_function() -> None:
    store.reset()


def test_demo_injection_flow_updates_single_case() -> None:
    response = client.get("/api/case/active")
    assert response.status_code == 200
    assert response.json()["state"] is None

    response = client.post("/api/demo/inject", json={"event_id": "CY-0213-001"})
    observe_case = response.json()
    assert response.status_code == 200
    assert observe_case["case_id"] == "CASE-GOLD-001"
    assert observe_case["state"] == "Observe"

    response = client.post("/api/demo/inject", json={"event_id": "AC-0224-001"})
    verify_case = response.json()
    assert response.status_code == 200
    assert verify_case["case_id"] == "CASE-GOLD-001"
    assert verify_case["state"] == "Verify Now"

    response = client.post("/api/demo/inject", json={"event_id": "IR-0231-001"})
    escalate_case = response.json()
    assert response.status_code == 200
    assert escalate_case["case_id"] == "CASE-GOLD-001"
    assert escalate_case["state"] == "Escalate Now"
    assert escalate_case["escalation_recommendation"] == "Notify protective services leadership and SOC now."


def test_unknown_event_id_returns_400() -> None:
    response = client.post("/api/demo/inject", json={"event_id": "NOPE"})
    assert response.status_code == 400
