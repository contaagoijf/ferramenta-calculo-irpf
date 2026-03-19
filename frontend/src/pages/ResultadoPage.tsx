import { useLocation, useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { CalculoInput, CalculoResultado, criarCalculo } from "../api";
import { useState } from "react";

type LocationState = {
  input?: CalculoInput;
  resultado?: CalculoResultado;
};

export default function ResultadoPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LocationState | null;

  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  if (!state?.input || !state.resultado) {
    return (
      <Layout>
        <div className="card">
          <h2>Resultado</h2>
          <p>Dados não encontrados. Inicie uma simulação para ver os resultados.</p>
          <button className="button" onClick={() => navigate("/calculo/ajuste-anual")}>Retornar ao formulário</button>
        </div>
      </Layout>
    );
  }

  const { input, resultado } = state;

  async function handleFinalizar() {
    setError(null);
    setSaving(true);
    try {
      const created = await criarCalculo(input);
      navigate(`/relatorio/${created.id}?calculo_novo=sim`);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Erro ao salvar o cálculo.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Layout>
      <div className="card">
        <h2>Resultado da simulação</h2>
        {error ? <div className="alert">{error}</div> : null}

        <table className="table">
          <tbody>
            <tr>
              <th>Base de cálculo</th>
              <td>{resultado.base_calculo}</td>
            </tr>
            <tr>
              <th>Imposto devido</th>
              <td>{resultado.imposto_devido}</td>
            </tr>
            <tr>
              <th>Imposto pago</th>
              <td>{resultado.imposto_pago}</td>
            </tr>
            <tr>
              <th>Saldo</th>
              <td>
                {resultado.saldo} ({resultado.tipo_saldo})
              </td>
            </tr>
          </tbody>
        </table>

        <div style={{ display: "flex", gap: "0.75rem", marginTop: "1rem" }}>
          <button className="button secondary" onClick={() => navigate(-1)}>
            Editar
          </button>
          <button className="button" onClick={handleFinalizar} disabled={saving}>
            {saving ? "Salvando..." : "Finalizar"}
          </button>
        </div>
      </div>
    </Layout>
  );
}
