from fastapi.testclient import TestClient
from unittest.mock import Mock
from app.main import app

def test_simulate_return_200(monkeypatch):
    monkeypatch.setattr("app.api.routes.simulate.run_risk_audit", Mock(return_value=None))

    client = TestClient(app)
    r = client.post("/simulate", json={"amount":1000, "annual_rate":12, "term_months":12})
    assert r.status_code == 200
    body = r.json()
    assert "schedule" in body and len(body["schedule"]) == 12