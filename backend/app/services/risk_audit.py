import random
import time
import logging

logger = logging.getLogger("creditsim.risk_audit")

def run_risk_audit(simulation_id: str) -> None:
    delay = random.randint(1, 3)
    time.sleep(delay)

    if random.random() < 0.10:
        raise RuntimeError(f"Risk audit failed for simulation {simulation_id}")
    
    logger.info("Risk audit OK for simulation_id=%s (delay=%.2fs)", simulation_id, delay)
