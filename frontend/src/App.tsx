import { Route, Routes, Navigate } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CalculadoraPage from "./pages/CalculadoraPage";
import ResultadoPage from "./pages/ResultadoPage";
import RelatorioPage from "./pages/RelatorioPage";
import ConsultaPage from "./pages/ConsultaPage";
import ParametrosPage from "./pages/ParametrosPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/calculo/ajuste-anual" element={<CalculadoraPage />} />
      <Route path="/resultado" element={<ResultadoPage />} />
      <Route path="/relatorio/:id" element={<RelatorioPage />} />
      <Route path="/consulta" element={<ConsultaPage />} />
      <Route path="/parametros" element={<ParametrosPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
