-- Schema for Ferramenta de Cálculo IRPF

-- Tabela de cálculos
CREATE TABLE IF NOT EXISTS calculos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  processo uuid NOT NULL,
  tipo_calculo text NOT NULL,
  ano_calendario int NOT NULL,
  dados_entrada jsonb NOT NULL,
  resultado jsonb,
  criado_em timestamptz NOT NULL DEFAULT now()
);

-- Parâmetros de IR por ano
CREATE TABLE IF NOT EXISTS ir_parametros (
  ano_calendario int PRIMARY KEY,
  teto numeric(18,2) NOT NULL,
  inicio_correcao date NOT NULL
);

-- Faixas de IR por ano
CREATE TABLE IF NOT EXISTS ir_faixas (
  id serial PRIMARY KEY,
  ano_calendario int NOT NULL REFERENCES ir_parametros(ano_calendario) ON DELETE CASCADE,
  limite_inferior numeric(18,2) NOT NULL,
  limite_superior numeric(18,2) NOT NULL,
  aliquota numeric(10,4) NOT NULL,
  deducao numeric(18,2) NOT NULL
);
