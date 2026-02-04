from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import List, Dict

getcontext().prec = 28 

def calculate_french_amortization(
    amount: Decimal,
    annual_rate: Decimal,
    term_months: int,
) -> Dict:
    if amount <= 0 or annual_rate < 0 or term_months <= 0:
        raise ValueError("Amount, annual rate, and term must be positive values.")
    
    monthly_rate = (annual_rate / Decimal('100')) / Decimal('12')
    
    if monthly_rate == 0:
        payment = amount / Decimal(term_months)
    else:
        payment = (
            amount 
            * (monthly_rate * (1 + monthly_rate) ** term_months)
            / ((1 + monthly_rate) ** term_months - 1)
        )
    
    payment = payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    balance = amount 
    schedule: List[Dict] = []

    total_interest = Decimal('0.00')

    for month in range(1, term_months + 1):
        interest = (balance * monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)        
        
        if month == term_months:
            principal = balance
            payment_final = (principal + interest).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            remaining_balance = Decimal('0.00')
        else: 
            principal = (payment - interest).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            payment_final = payment
            remaining_balance = (balance - principal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        total_interest += interest

        schedule.append(
            {
                "month": month,
                "payment": payment_final,
                "principal": principal,
                "interest": interest,
                "remaining_balance": remaining_balance,
            }
        )

        balance = remaining_balance
    
    total_payment = (amount + total_interest).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        "summary": {
            "monthly_payment": payment,
            "total_interest": total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            "total_payment": total_payment,
        },
        "schedule": schedule,
    }