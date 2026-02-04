import { money } from "../lib/format";

export default function AmortizationTable({ schedule }) {
  if (!schedule?.length) return null;

  return (
    <div className="card tableCard">
      <div className="cardHeader compact">
        <div>
          <h3 className="cardTitle">Tabla de amortización</h3>
          <p className="cardSubtitle">Pago fijo, interés decreciente.</p>
        </div>
      </div>

      <div className="tableWrap">
        <table className="table">
          <thead>
            <tr>
              <th>Mes</th>
              <th>Pago</th>
              <th>Pago principal</th>
              <th>Interes</th>
              <th>Saldo restante</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((r) => (
              <tr key={r.month}>
                <td className="mono">{r.month}</td>
                <td>{money(r.payment)}</td>
                <td>{money(r.principal)}</td>
                <td>{money(r.interest)}</td>
                <td>{money(r.remaining_balance)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
