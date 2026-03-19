-- Seed data example for IR parameters and faixas

INSERT INTO ir_parametros (ano_calendario, teto, inicio_correcao)
VALUES
  (2024, 60000.00, '2024-01-01')
ON CONFLICT (ano_calendario) DO NOTHING;

INSERT INTO ir_faixas (ano_calendario, limite_inferior, limite_superior, aliquota, deducao)
VALUES
  (2024, 0.00, 22847.76, 0.0, 0.00),
  (2024, 22847.77, 33919.80, 0.075, 1713.58),
  (2024, 33919.81, 45012.60, 0.15, 4257.57),
  (2024, 45012.61, 55976.16, 0.225, 7633.51),
  (2024, 55976.17, 999999999.99, 0.275, 10432.32)
ON CONFLICT DO NOTHING;
