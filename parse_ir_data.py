try:
    import requests
except ImportError:
    requests = None

import hashlib
import difflib
import os

# URL do arquivo TXT
url = "https://www.trf2.jus.br/sites/default/publico/JFRJ/arquivos/filefieldreplice/calculos/009irpfa.txt"

# Caminho do arquivo seed.sql
seed_file = 'backend/db/seed.sql'

# Baixar o conteúdo
if requests is not None:
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
else:
    import urllib.request
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8', errors='replace')

content = content.replace('\r', '')
lines = [ln.strip() for ln in content.split('\n') if ln.strip()]

# Verificar se seed.sql existe e calcular hash antigo
hash_antigo = None
conteudo_antigo = None
if os.path.exists(seed_file):
    with open(seed_file, 'r', encoding='utf-8') as f:
        conteudo_antigo = f.read()
    hash_antigo = hashlib.sha256(conteudo_antigo.encode('utf-8')).hexdigest()

# Dicionários para armazenar dados
ir_parametros = []
ir_faixas = []

# Processar cada linha
for line in lines:
    if not line.strip():
        continue
    fields = line.split('\t')
    if len(fields) < 2:
        continue
    try:
        ano = int(fields[0])
        if ano < 1990 or ano > 2025:
            continue  # Apenas anos de 1990 a 2025
        tipo = fields[1]
        if tipo not in ('MOEDA', 'UFIR'):
            continue
        
        # Os próximos campos são os 5 grupos de faixa: % min deducao
        faixa_fields = fields[2:-2]  # Exclui ano, tipo, teto, data
        faixas = []
        for i in range(0, len(faixa_fields), 3):
            pct = faixa_fields[i].strip()
            min_val_str = faixa_fields[i+1].strip()
            deducao_str = faixa_fields[i+2].strip()

            aliquota = float(pct.rstrip('%').replace(',', '.')) / 100
            min_val = float(min_val_str.replace('.', '').replace(',', '.'))
            deducao = float(deducao_str.replace('.', '').replace(',', '.'))

            faixas.append((aliquota, min_val, deducao))

        # Remover duplicatas de mesma faixa (ex.: múltiplos 0%, 0,00)
        unique_faixas = list({(a, m, d): None for a, m, d in faixas}.keys())

        # Ordenar por limite inferior crescente
        unique_faixas.sort(key=lambda x: x[1])

        faixas_processadas = unique_faixas

        # Construir as tuplas para ir_faixas
        for idx, (aliquota, min_val, deducao) in enumerate(faixas_processadas):
            if idx == 0:
                limite_inferior = 0.00
            else:
                limite_inferior = faixas_processadas[idx][1]

            if idx == len(faixas_processadas) - 1:
                limite_superior = 'NULL'
            else:
                proximo_min = faixas_processadas[idx + 1][1]
                limite_superior = round(proximo_min - 0.01, 2)

            if limite_superior != 'NULL':
                ir_faixas.append(
                    f"({ano}, {limite_inferior:.2f}, {limite_superior:.2f}, {aliquota:.3f}, {deducao:.2f})"
                )
            else:
                ir_faixas.append(
                    f"({ano}, {limite_inferior:.2f}, NULL, {aliquota:.3f}, {deducao:.2f})"
                )
        
        # ir_parametros: teto e inicio_correcao
        teto_str = fields[-2].strip()
        teto = float(teto_str.replace('.', '').replace(',', '.'))
        data_str = fields[-1].strip()  # DD/MM/YYYY
        dia, mes, ano_data = [p.strip() for p in data_str.split('/')]
        inicio_correcao = f"{ano_data}-{mes.zfill(2)}-{dia.zfill(2)}"
        ir_parametros.append(f"({ano}, {teto:.2f}, '{inicio_correcao}')")
        
    except (ValueError, IndexError) as e:
        print(f"Erro ao processar linha: {line} - {e}")
        continue

# Escrever o arquivo seed.sql
novo_conteudo = "-- Seed data for IR parameters and faixas from TRF2 (1990-2025)\n"
novo_conteudo += "-- Source: https://www.trf2.jus.br/sites/default/publico/JFRJ/arquivos/filefieldreplice/calculos/009irpfa.txt\n\n"

novo_conteudo += "INSERT INTO ir_parametros (ano_calendario, teto, inicio_correcao) VALUES\n"
novo_conteudo += ',\n'.join(ir_parametros)
novo_conteudo += "\nON CONFLICT (ano_calendario) DO NOTHING;\n\n"

novo_conteudo += "INSERT INTO ir_faixas (ano_calendario, limite_inferior, limite_superior, aliquota, deducao) VALUES\n"
# Agrupar por ano
faixas_por_ano = {}
for faixa in ir_faixas:
    ano = int(faixa.split(',')[0][1:])
    if ano not in faixas_por_ano:
        faixas_por_ano[ano] = []
    faixas_por_ano[ano].append(faixa)

all_faixas = []
for ano in sorted(faixas_por_ano.keys()):
    all_faixas.append(f"-- {ano}")
    all_faixas.extend(faixas_por_ano[ano])

novo_conteudo += ',\n'.join(all_faixas)
novo_conteudo += "\nON CONFLICT DO NOTHING;\n"

# Calcular hash do novo conteúdo
hash_novo_conteudo = hashlib.sha256(novo_conteudo.encode('utf-8')).hexdigest()

# Se hashes iguais, não fazer nada
if hash_antigo == hash_novo_conteudo:
    print("O arquivo seed.sql já está atualizado. Nenhuma alteração necessária.")
    exit(0)

# Se houve mudança, escrever e logar diff
with open(seed_file, 'w', encoding='utf-8') as f:
    f.write(novo_conteudo)

print("Arquivo seed.sql atualizado com sucesso!")

# Logar diff
if conteudo_antigo is not None:
    diff = difflib.unified_diff(
        conteudo_antigo.splitlines(keepends=True),
        novo_conteudo.splitlines(keepends=True),
        fromfile='seed.sql (antigo)',
        tofile='seed.sql (novo)',
        lineterm=''
    )
    print("\nDiferenças encontradas:")
    print(''.join(diff))
else:
    print("Arquivo seed.sql criado pela primeira vez.")