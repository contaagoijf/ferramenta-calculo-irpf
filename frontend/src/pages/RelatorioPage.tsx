import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import Layout from "../components/Layout";
import { baixarPdf, buscarCalculo, CalculoPersistido } from "../api";

export default function RelatorioPage() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [calculo, setCalculo] = useState<CalculoPersistido | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isNovo = useMemo(() => searchParams.get("calculo_novo") === "sim", [searchParams]);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    buscarCalculo(id)
      .then((data) => setCalculo(data))
      .catch(() => setError("Falha ao buscar o cálculo. Verifique o ID e tente novamente."))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleExportPdf() {
    if (!id) return;
    const data = await baixarPdf(id);
    const blob = new Blob([data], { type: "application/pdf" });
    const fileUrl = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = fileUrl;
    a.download = `relatorio_${id}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(fileUrl);
  }

  function handleRefazer() {
    if (!calculo) return;
    const tipo = calculo.tipo_calculo === "retificacao" ? "retificacao" : "ajuste_anual";
    navigate(`/calculo/ajuste-anual?id=${calculo.id}&tipo_calculo=${tipo}`);
  }

  if (loading) {
    return (
      <Layout>
        <div className="card">
          <p>Carregando...</p>
        </div>
      </Layout>
    );
  }

  if (error || !calculo) {
    return (
      <Layout>
        <div className="card">
          <h2>Relatório</h2>
          <div className="alert">{error ?? "Cálculo não encontrado."}</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="card">
        <h2>Relatório de cálculo</h2>
        <div style={{ marginBottom: "1rem" }}>
          <strong>Processo:</strong> {calculo.dados_entrada.processo} <br />
          <strong>Autor:</strong> {calculo.dados_entrada.nome_autor} <br />
          <strong>ID do cálculo:</strong> {calculo.id} <br />
          <strong>Ano calendário:</strong> {calculo.ano_calendario}
        </div>

        <h3>Resultado</h3>
        <table className="table">
          <tbody>
            <tr>
              <th>Base de cálculo</th>
              <td>{calculo.resultado?.base_calculo}</td>
            </tr>
            <tr>
              <th>Imposto devido</th>
              <td>{calculo.resultado?.imposto_devido}</td>
            </tr>
            <tr>
              <th>Imposto pago</th>
              <td>{calculo.resultado?.imposto_pago}</td>
            </tr>
            <tr>
              <th>Saldo</th>
              <td>
                {calculo.resultado?.saldo} ({calculo.resultado?.tipo_saldo})
              </td>
            </tr>
          </tbody>
        </table>

        <div style={{ display: "flex", gap: "0.75rem", marginTop: "1rem" }}>
          <button className="button" onClick={handleExportPdf}>
            Exportar PDF
          </button>
          {!isNovo ? (
            <button className="button secondary" onClick={handleRefazer}>
              Refazer cálculo
            </button>
          ) : null}
        </div>
      </div>
    </Layout>
  );
}
