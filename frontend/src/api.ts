import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export type CalculoInput = {
  processo: string;
  nome_autor: string;
  tipo_declaracao: "completa" | "simplificada";
  ano_calendario: number;
  rendimentos_tributaveis: number;
  deducoes_legais: number;
  deducoes_incentivo: number;
  imposto_rra: number;
  imposto_pago: number;
  rend_somar: number;
  rend_sub: number;
  ded_somar: number;
  ded_sub: number;
  incentivo_somar: number;
  incentivo_sub: number;
  rra_somar: number;
  rra_sub: number;
  tipo_calculo: "ajuste_anual" | "retificacao";
};

export type CalculoResultado = {
  base_calculo: number;
  imposto_devido: number;
  imposto_pago: number;
  saldo: number;
  tipo_saldo: string;
  detalhes: Record<string, any>;
};

export type CalculoPersistido = {
  id: string;
  processo: string;
  tipo_calculo: string;
  ano_calendario: number;
  dados_entrada: CalculoInput;
  resultado?: CalculoResultado;
  criado_em: string;
};

export type IrFaixa = {
  id: number;
  ano_calendario: number;
  limite_inferior: number;
  limite_superior: number;
  aliquota: number;
  deducao: number;
};

export type IrParametros = {
  ano_calendario: number;
  teto: number;
  inicio_correcao: string;
  faixas: IrFaixa[];
};

export async function simularCalculo(input: CalculoInput) {
  const { data } = await client.post<CalculoResultado>("/calculos/simular", input);
  return data;
}

export async function criarCalculo(input: CalculoInput) {
  const { data } = await client.post<CalculoPersistido>("/calculos", input);
  return data;
}

export async function buscarCalculo(id: string) {
  const { data } = await client.get<CalculoPersistido>(`/calculos/${id}`);
  return data;
}

export async function baixarPdf(id: string) {
  const response = await client.get<ArrayBuffer>(`/calculos/${id}/pdf`, {
    responseType: "arraybuffer",
  });
  return response.data;
}

export async function buscarParametros(ano: number) {
  const { data } = await client.get<IrParametros>(`/parametros/${ano}`);
  return data;
}

export async function salvarParametros(parametros: IrParametros) {
  const { data } = await client.put<IrParametros>(`/parametros/${parametros.ano_calendario}`, parametros);
  return data;
}
