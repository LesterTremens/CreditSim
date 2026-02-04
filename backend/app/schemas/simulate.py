from decimal import Decimal
from pydantic import BaseModel, Field

class SimulateRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    annual_rate: Decimal = Field(..., ge=0)
    term_months: int = Field(..., gt=0)

    