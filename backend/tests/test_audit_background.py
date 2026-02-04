from fastapi import BackgroundTasks
from unittest.mock import Mock
from app.api.routes.simulate import simulate
from app.schemas.simulate import SimulateRequest
import uuid

class DummyDB:
    def add(self, obj): pass
    def commit(self): pass
    def refresh(self, obj):
        obj.id = uuid.uuid4()

def test_audit_background_task(monkeypatch):
    
    audit_mock = Mock(side_effect=RuntimeError("Should not be called inline"))
    monkeypatch.setattr("app.services.risk_audit.run_risk_audit", audit_mock)

    payload = SimulateRequest(amount=1000, annual_rate=12, term_months=12)
    bg = BackgroundTasks()
    db = DummyDB()

    simulate(payload=payload, background_tasks=bg, db=db)
    audit_mock.assert_not_called()
    assert len(bg.tasks) == 1