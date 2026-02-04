from app.models.simulation import Simulation

def test_simulation_is_persisted(client, db_session):
    response = client.post(
        "/simulate",
        json={
            "amount": 10000,
            "annual_rate": 10,
            "term_months": 12,
        },
    )

    assert response.status_code == 200

    simulations = db_session.query(Simulation).all()
    assert len(simulations) == 1

    sim = simulations[0]
    assert float(sim.amount) == 10000
    assert float(sim.annual_rate) == 10
    assert int(sim.term_months) == 12