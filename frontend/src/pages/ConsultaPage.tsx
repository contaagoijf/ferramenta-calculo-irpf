import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";

export default function ConsultaPage() {
  const [id, setId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!id.trim()) {
      setError("Informe um ID válido.");
      return;
    }
    setError(null);
    navigate(`/relatorio/${id.trim()}`);
  }

  return (
    <Layout>
      <div className="card">
        <h2>Consultar cálculo por ID</h2>
        {error ? <div className="alert">{error}</div> : null}
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>ID do cálculo</label>
            <input value={id} onChange={(ev) => setId(ev.target.value)} required />
          </div>
          <button className="button" type="submit">
            Buscar
          </button>
        </form>
      </div>
    </Layout>
  );
}
