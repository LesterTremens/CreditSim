from decimal import Decimal
import pytest

from app.services.amortization import calculate_french_amortization

def test_basic_amortization_calculation():
    result = calculate_french_amortization(
        amount=Decimal('100000'),
        annual_rate=Decimal('12'),
        term_months=24,
    )

    assert "summary" in result
    assert "schedule" in result 
    assert len(result["schedule"]) == 24

    first_month = result["schedule"][0]
    last_month = result["schedule"][-1]

    assert first_month["month"] == 1
    assert last_month["remaining_balance"] == Decimal("0.00")

def test_zero_interest_rate():
    result = calculate_french_amortization(
        amount=Decimal('12000'),
        annual_rate=Decimal('0'),
        term_months=12,
    )

    for row in result["schedule"]:
        assert row["interest"] == Decimal('0.00')

    assert result["summary"]["total_interest"] == Decimal('0.00')

def test_total_principal_equals_amount():
    amount = Decimal('50000')

    result = calculate_french_amortization(
        amount=amount,
        annual_rate=Decimal('10'),
        term_months=10,
    )

    total_principal = sum(row["principal"] for row in result["schedule"])
    assert total_principal.quantize(Decimal("0.01")) == amount

def test_invalid_amount_raises_error():
    with pytest.raises(ValueError):
        calculate_french_amortization(
            amount=Decimal("0"),
            annual_rate=Decimal("10"),
            term_months=12,
        )


