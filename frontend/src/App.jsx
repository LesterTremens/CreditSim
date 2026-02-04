import { useMemo, useState } from "react";
import { useLocalStorageState } from "./hooks/useLocalStorageState";
import { simulateCredit } from "./lib/api";

import SimulatorForm from "./components/SimulatorForm";
import SummaryCards from "./components/SummaryCards";
import AmortizationTable from "./components/AmortizationTable";

const LS_KEY = "creditsim_form_v1";
const LS_RESULT_KEY = "creditsim_result_v1";

const defaultForm = {
  amount: "",
  annual_rate: "",
  term_months: "",
};

export default function App() {
  const apiUrl = useMemo(() => import.meta.env.VITE_API_URL, []);
  const [form, setForm] = useLocalStorageState(LS_KEY, defaultForm);

  const [result, setResult] = useState(() => {
    try {
      const raw = localStorage.getItem(LS_RESULT_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function clearResult() {
    setResult(null);
    localStorage.removeItem(LS_RESULT_KEY);
  }

  function onChange(e) {
    const { name, value } = e.target;

    setForm((prev) => {
      const next = { ...prev, [name]: value };

      if (name === "amount" || name === "annual_rate" || name === "term_months") {
        clearResult();
      }

      return next;
    });
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    clearResult();

    try {
      const payload = {
        amount: Number(form.amount),
        annual_rate: Number(form.annual_rate),
        term_months: Number(form.term_months),
      };

      const data = await simulateCredit(apiUrl, payload);
      setResult(data);
      localStorage.setItem(LS_RESULT_KEY, JSON.stringify(data));
    } catch (err) {
      setError(err?.message ?? "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="topbar">
        <div>
          <h1 className="title">CreditSim</h1>
        </div>
      </header>

      <main>
        <div className="stack">
          <SimulatorForm
            value={form}
            onChange={onChange}
            onSubmit={onSubmit}
            loading={loading}
            hasResult={Boolean(result)}
          />

          {error ? (
            <div className="alert">
              <b>Error:</b> {error}
            </div>
          ) : null}

          <SummaryCards
            summary={result?.summary}
            simulationId={result?.simulation_id}
          />

          <AmortizationTable schedule={result?.schedule} />
        </div>
      </main>
    </div>
  );
}
