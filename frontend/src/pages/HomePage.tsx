import { Link } from "react-router-dom";
import Layout from "../components/Layout";

export default function HomePage() {
  return (
    <Layout>
      <div className="card">
        <h2>Ferramenta de Cálculo para Ajuste e Retificação de IRPF</h2>
        <p>
          Use a ferramenta para simular e gerar relatórios de ajustes de IRPF. Os
          cálculos são determinísticos e a saída pode ser exportada como PDF.
        </p>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <Link to="/calculo/ajuste-anual" className="button">
            Ajuste Anual
          </Link>
          <Link
            to="/calculo/ajuste-anual?tipo_calculo=retificacao"
            className="button"
          >
            Retificação de IRPF
          </Link>
          <Link to="/consulta" className="button secondary">
            Buscar cálculo por ID
          </Link>
        </div>
      </div>
    </Layout>
  );
}
