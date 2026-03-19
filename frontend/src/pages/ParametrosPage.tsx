import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { buscarParametros, salvarParametros, IrParametros, IrFaixa } from "../api";

export default function ParametrosPage() {
  const [ano, setAno] = useState(new Date().getFullYear());
  const [parametros, setParametros] = useState<IrParametros | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadParametros(ano);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function loadParametros(anoBusca: number) {
    setLoading(true);
    setError(null);

    try {
      const data = await buscarParametros(anoBusca);
      setParametros(data);
    } catch (err: any) {
      setParametros(null);
      setError(err?.response?.data?.detail || "Não foi possível carregar os parâmetros.");
    } finally {
      setLoading(false);
    }
  }

  async function handleBuscar(event: React.FormEvent) {
    event.preventDefault();
    loadParametros(ano);
  }

  function handleFaixaChange(index: number, field: keyof IrFaixa, value: string) {
    if (!parametros) return;
    const updated = { ...parametros };
    const list = [...updated.faixas];
    const faixa = { ...list[index] };
    faixa[field] = field === "ano_calendario" || field === "id" ? Number(value) : Number(value);
    list[index] = faixa;
    updated.faixas = list;
    setParametros(updated);
  }

  async function handleSave() {
    if (!parametros) return;
    setSaving(true);
    setError(null);
    try {
      const saved = await salvarParametros(parametros);
      setParametros(saved);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Falha ao salvar parâmetros.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Layout>
      <div className="card">
        <h2>Parâmetros de IR</h2>

        <form onSubmit={handleBuscar} style={{ marginBottom: "1rem" }}>
          <div className="field">
            <label>Ano calendário</label>
            <input
              type="number"
              value={ano}
              onChange={(ev) => setAno(Number(ev.target.value))}
            />
          </div>
          <button className="button" type="submit">
            Buscar
          </button>
        </form>

        {loading && <p>Carregando parâmetros...</p>}
        {error && <div className="alert">{error}</div>}

        {parametros ? (
          <>
            <div className="field">
              <label>Teto</label>
              <input
                type="number"
                value={parametros.teto}
                onChange={(ev) =>
                  setParametros((prev) => (prev ? { ...prev, teto: Number(ev.target.value) } : prev))
                }
              />
            </div>
            <div className="field">
              <label>Data de correção</label>
              <input
                type="date"
                value={parametros.inicio_correcao}
                onChange={(ev) =>
                  setParametros((prev) => (prev ? { ...prev, inicio_correcao: ev.target.value } : prev))
                }
              />
            </div>

            <h3>Faixas de IR</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>Limite inferior</th>
                  <th>Limite superior</th>
                  <th>Alíquota</th>
                  <th>Dedução</th>
                </tr>
              </thead>
              <tbody>
                {parametros.faixas.map((faixa, idx) => (
                  <tr key={faixa.id}>
                    <td>
                      <input
                        type="number"
                        value={faixa.limite_inferior}
                        onChange={(ev) => handleFaixaChange(idx, "limite_inferior", ev.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        value={faixa.limite_superior}
                        onChange={(ev) => handleFaixaChange(idx, "limite_superior", ev.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.0001"
                        value={faixa.aliquota}
                        onChange={(ev) => handleFaixaChange(idx, "aliquota", ev.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        value={faixa.deducao}
                        onChange={(ev) => handleFaixaChange(idx, "deducao", ev.target.value)}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div style={{ marginTop: "1rem" }}>
              <button className="button" disabled={saving} onClick={handleSave}>
                {saving ? "Salvando..." : "Salvar parâmetros"}
              </button>
            </div>
          </>
        ) : null}
      </div>
    </Layout>
  );
}
