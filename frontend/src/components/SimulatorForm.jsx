export default function SimulatorForm({
    value,
    onChange,
    onSubmit,
    loading,
    hasResult,
  }) {
    return (
      <form onSubmit={onSubmit} className="card">
        <div className="cardHeader">
          <div>
            <h2 className="cardTitle">Simulación</h2>
            <p className="cardSubtitle">
                Introduzca los detalles del préstamo para generar una la tabla de amortización.
            </p>
          </div>
  
          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Calculando..." : "Calcular"}
          </button>
        </div>
  
        <div className="grid3">
          <Field label="Monto" hint="Monto principal">
            <input
              name="amount"
              value={value.amount}
              onChange={onChange}
              inputMode="decimal"
              placeholder="e.g. 100000"
              required
              type="number"
            />
          </Field>
  
          <Field label="Tasa anual (%)" hint="Tasa nominal anual">
            <input
              type="number"
              name="annual_rate"
              value={value.annual_rate}
              onChange={onChange}
              inputMode="decimal"
              placeholder="e.g. 12.5"
              required
            />
          </Field>
  
          <Field label="Plazo (meses)" hint="Número total de pagos">
            <input
              type="number"
              name="term_months"
              value={value.term_months}
              onChange={onChange}
              inputMode="numeric"
              placeholder="e.g. 24"
              required
            />
          </Field>
        </div>
  
        {hasResult ? (
          <div className="note">
            Tip: Si tu cambias el <b>monto</b>, <b>tasa anual</b> o el <b>plazo</b> los resultados seran borrados. 
          </div>
        ) : null}
      </form>
    );
  }
  
  function Field({ label, hint, children }) {
    return (
      <label className="field">
        <span className="fieldLabel">{label}</span>
        <span className="fieldHint">{hint}</span>
        {children}
      </label>
    );
  }
  