import { Link } from "react-router-dom";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="container">
      <header className="header">
        <h1>Ferramenta de Cálculo IRPF</h1>
        <nav className="nav">
          <Link to="/" className="navLink">
            Início
          </Link>
          <Link to="/parametros" className="navLink">
            Parâmetros
          </Link>
        </nav>
      </header>
      <main className="main">{children}</main>
      <footer className="footer">
        <small>Ferramenta de Cálculo IRPF • MVP</small>
      </footer>
    </div>
  );
}
