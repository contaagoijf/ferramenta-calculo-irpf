import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Layout from "../components/Layout";
import { CalculoInput, CalculoResultado, buscarCalculo, simularCalculo } from "../api";

const DEFAULT_INPUT: CalculoInput = {
  processo: "",
  nome_autor: "",
  tipo_declaracao: "completa",
  ano_calendario: new Date().getFullYear(),
  rendimentos_tributaveis: 0,
  deducoes_legais: 0,
  deducoes_incentivo: 0,
  imposto_rra: 0,
  imposto_pago: 0,
  rend_somar: 0,
  rend_sub: 0,
  ded_somar: 0,
  ded_sub: 0,
  incentivo_somar: 0,
  incentivo_sub: 0,
  rra_somar: 0,
  rra_sub: 0,
  tipo_calculo: "ajuste_anual",
};

function asNumber(value: string | number) {
  const str = String(value).replace(',', '.');
  const num = Number(str);
  return Number.isNaN(num) ? 0 : num;
}

export default function CalculadoraPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [input, setInput] = useState<CalculoInput>(DEFAULT_INPUT);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resultado, setResultado] = useState<CalculoResultado | null>(null);

  const tipoCalculo = useMemo(() => {
    const tipo = searchParams.get("tipo_calculo") || "ajuste_anual";
    return tipo === "retificacao" ? "retificacao" : "ajuste_anual";
  }, [searchParams]);

  const calculoId = useMemo(() => searchParams.get("id") || undefined, [searchParams]);

  useEffect(() => {
    setInput((current) => ({ ...current, tipo_calculo: tipoCalculo }));
  }, [tipoCalculo]);

  useEffect(() => {
    if (!calculoId) return;

    setLoading(true);
    buscarCalculo(calculoId)
      .then((calculo) => {
        setInput({
          ...calculo.dados_entrada,
          tipo_calculo: calculo.tipo_calculo as "ajuste_anual" | "retificacao",
        });
        setResultado(calculo.resultado ?? null);
      })
      .catch(() => {
        setError("Não foi possível carregar o cálculo. Verifique o ID e tente novamente.");
      })
      .finally(() => setLoading(false));
  }, [calculoId]);

  function handleChange<K extends keyof CalculoInput>(key: K, value: string) {
    if (key === "processo" || key === "nome_autor" || key === "tipo_declaracao") {
      setInput((prev) => ({
        ...prev,
        [key]: value,
      }));
    } else {
      setInput((prev) => ({
        ...prev,
        [key]: asNumber(value),
      }));
    }
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    simularCalculo(input)
      .then((res) => {
        setResultado(res);
        navigate("/resultado", { state: { input, resultado: res } });
      })
      .catch((err) => {
        let errorMsg = "Falha ao simular cálculo.";
        if (err?.response?.data?.detail) {
          errorMsg = err.response.data.detail;
        } else if (err?.response?.data?.errors) {
          // Capturar erros de validação Pydantic
          const errors = err.response.data.errors;
          if (Array.isArray(errors)) {
            errorMsg = errors.map((e: any) => `${e.loc?.join(".")}: ${e.msg}`).join("; ");
          }
        } else if (err?.response?.status === 422) {
          errorMsg = "Erro de validação. Verifique os valores informados.";
        }
        setError(errorMsg);
      })
      .finally(() => setLoading(false));
  }

  const showDeductionFields = input.tipo_declaracao === "completa";

  return (
    <Layout>
      <div className="card">
        <h2>Simulação de cálculo ({tipoCalculo.replace("_", " ")})</h2>

        {error ? <div className="alert">{error}</div> : null}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Número do processo (UUID)</label>
            <input
              value={input.processo}
              onChange={(ev) => handleChange("processo", ev.target.value)}
              required
              placeholder="00000000-0000-0000-0000-000000000000"
            />
          </div>

          <div className="field">
            <label>Nome do autor</label>
            <input
              value={input.nome_autor}
              onChange={(ev) => handleChange("nome_autor", ev.target.value)}
              required
            />
          </div>

          <div className="field">
            <label>Tipo de declaração</label>
            <select
              value={input.tipo_declaracao}
              onChange={(ev) => handleChange("tipo_declaracao", ev.target.value)}
            >
              <option value="completa">Completa</option>
              <option value="simplificada">Simplificada</option>
            </select>
          </div>

          <div className="field">
            <label>Ano calendário</label>
            <input
              type="number"
              value={input.ano_calendario}
              min={1900}
              onChange={(ev) => handleChange("ano_calendario", ev.target.value)}
            />
          </div>

          <div className="field">
            <label>Rendimentos tributáveis</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.rendimentos_tributaveis}
              onChange={(ev) => handleChange("rendimentos_tributaveis", ev.target.value)}
            />
          </div>

          {showDeductionFields ? (
            <>
              <div className="field">
                <label>Deduções legais</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.deducoes_legais}
                  onChange={(ev) => handleChange("deducoes_legais", ev.target.value)}
                />
              </div>
              <div className="field">
                <label>Deduções de incentivo</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.deducoes_incentivo}
                  onChange={(ev) => handleChange("deducoes_incentivo", ev.target.value)}
                />
              </div>
            </>
          ) : null}

          <div className="field">
            <label>Imposto RRA</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.imposto_rra}
              onChange={(ev) => handleChange("imposto_rra", ev.target.value)}
            />
          </div>

          <div className="field">
            <label>Imposto pago</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.imposto_pago}
              onChange={(ev) => handleChange("imposto_pago", ev.target.value)}
            />
          </div>

          <h3>Ajustes</h3>

          <div className="field">
            <label>Rendimentos a somar</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.rend_somar}
              onChange={(ev) => handleChange("rend_somar", ev.target.value)}
            />
          </div>
          <div className="field">
            <label>Rendimentos a subtrair</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.rend_sub}
              onChange={(ev) => handleChange("rend_sub", ev.target.value)}
            />
          </div>

          {showDeductionFields ? (
            <>
              <div className="field">
                <label>Deduções legais a somar</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.ded_somar}
                  onChange={(ev) => handleChange("ded_somar", ev.target.value)}
                />
              </div>
              <div className="field">
                <label>Deduções legais a subtrair</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.ded_sub}
                  onChange={(ev) => handleChange("ded_sub", ev.target.value)}
                />
              </div>
              <div className="field">
                <label>Incentivos a somar</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.incentivo_somar}
                  onChange={(ev) => handleChange("incentivo_somar", ev.target.value)}
                />
              </div>
              <div className="field">
                <label>Incentivos a subtrair</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={input.incentivo_sub}
                  onChange={(ev) => handleChange("incentivo_sub", ev.target.value)}
                />
              </div>
            </>
          ) : null}

          <div className="field">
            <label>Imposto devido RRA a somar</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.rra_somar}
              onChange={(ev) => handleChange("rra_somar", ev.target.value)}
            />
          </div>
          <div className="field">
            <label>Imposto devido RRA a subtrair</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={input.rra_sub}
              onChange={(ev) => handleChange("rra_sub", ev.target.value)}
            />
          </div>

          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
            <button type="submit" className="button" disabled={loading}>
              {loading ? "Simulando..." : "Simular"}
            </button>
            <button
              type="button"
              className="button secondary"
              onClick={() => {
                setResultado(null);
                setError(null);
              }}
            >
              Limpar
            </button>
          </div>
        </form>

        {resultado ? (
          <div style={{ marginTop: "1.5rem" }}>
            <h3>Resultado</h3>
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
                  <th>Saldo ({resultado.tipo_saldo})</th>
                  <td>{resultado.saldo}</td>
                </tr>
              </tbody>
            </table>
            <div style={{ marginTop: "1rem" }}>
              <button
                className="button"
                onClick={() =>
                  navigate("/resultado", { state: { input, resultado }, replace: true })
                }
              >
                Ver mais detalhes
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </Layout>
  );
}
