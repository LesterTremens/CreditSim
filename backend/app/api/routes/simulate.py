from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from app.services.risk_audit import run_risk_audit
from app.db.session import get_db
from app.models.simulation import Simulation
from app.schemas.simulate import SimulateRequest
from app.services.amortization import calculate_french_amortization
from app.api.routes.auth import get_current_user
from app.models.user import User

logger = logging.getLogger("creditsim.api")
router = APIRouter(tags=["simulate"])

def _to_json_safe(result: dict) -> dict:
    result["summary"]["monthly_payment"] = float(result["summary"]["monthly_payment"])
    result["summary"]["total_interest"] = float(result["summary"]["total_interest"])
    result["summary"]["total_payment"] = float(result["summary"]["total_payment"])

    for row in result["schedule"]:
        row["payment"] = float(row["payment"])
        row["principal"] = float(row["principal"])
        row["interest"] = float(row["interest"])
        row["remaining_balance"] = float(row["remaining_balance"])
    return result

@router.post("/simulate")
def simulate(
    payload: SimulateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = calculate_french_amortization(
        amount=payload.amount,
        annual_rate=payload.annual_rate,
        term_months=payload.term_months,
    )

    sim = Simulation(
        amount=float(payload.amount),
        annual_rate=float(payload.annual_rate),
        term_months=payload.term_months
    )

    db.add(sim)
    db.commit()
    db.refresh(sim)

    def _safe_audit():
        try:
            run_risk_audit(str(sim.id))
        except Exception:
            logger.exception("Risk audit error for simulation_id=%s", str(sim.id))
    
    background_tasks.add_task(_safe_audit)

    json_result = _to_json_safe(result)
    json_result["simulation_id"] = str(sim.id)
    return _to_json_safe(result)
