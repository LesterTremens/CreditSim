import { money } from "../lib/format";

export default function SummaryCards({ summary, simulationId }) {
  if (!summary) return null;

  return (
    <div className="card">
      <div className="cardHeader compact">
        <div>
          <h2 className="cardTitle">Resultados</h2>
          {simulationId ? (
            <p className="muted">
              Identificador de la operación: <span className="mono">{simulationId}</span>
            </p>
          ) : null}
        </div>
      </div>

      <div className="stats">
        <Stat label="Pago mensual" value={money(summary.monthly_payment)} />
        <Stat label="Interes total" value={money(summary.total_interest)} />
        <Stat label="Pago total" value={money(summary.total_payment)} />
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="stat">
      <div className="statLabel">{label}</div>
      <div className="statValue">{value}</div>
    </div>
  );
}
