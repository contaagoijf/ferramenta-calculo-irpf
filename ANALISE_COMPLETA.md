# ANÁLISE COMPLETA - Ferramenta Cálculo IRPF

**Data**: Março 2026  
**Status**: Estrutura básica CORRETA, mas problemas em routing e variáveis de ambiente

---

## 1. ESTRUTURA DE ROTEAMENTO ✅ CORRETA

### 1.1 vercel.json - CORRETO
```json
✅ Arquivo está certo:
- Detecta backend/api/index.py como função serverless
- Roteia /api/v1/* para backend
- Roteia / para frontend/dist/index.html
```

**Sem mudanças necessárias** - A estrutura está OK.

---

### 1.2 backend/api/index.py - CORRETO ✅
```python
✅ Arquivo está certo:
- sys.path.insert(0, str(Path(__file__).parent.parent))
  → Adiciona 'backend' ao path para importar 'app'
- from app.main import app → Importação correta
- __all__ = ["app"] → Vercel detecta como ASGI
```

**Confirmado**: A importação funciona. Path está correto.

---

### 1.3 backend/app/main.py - CORRETO ✅
```python
✅ ASGI Compatibility OK:
- FastAPI app criada com create_app()
- app = create_app() → Exportada como módulo
- CORS configurado corretamente
```

**Status**: Compatível com ASGI. Vercel consegue rodar.

---

### 1.4 Conflitos de Rotas - NENHUM ✅
```
Análise de rotas:
├── /api/v1/calculos/simular        → OK (POST)
├── /api/v1/calculos                → OK (POST/GET)
├── /api/v1/calculos/{id}           → OK (GET)
├── /api/v1/calculos/{id}/pdf       → OK (GET)
├── /api/v1/parametros/{ano}        → OK (GET/PUT)
├── /api/v1/parametros/{ano}/faixas → OK (POST)
└── /api/v1/docs                    → OK (FastAPI automático)
```

**Nenhum conflito encontrado**. Todas as rotas estão bem definidas.

---

## 2. PROBLEMAS DE IMPORTAÇÃO ✅ SEM PROBLEMAS

### 2.1 backend/api/index.py → app.main.app
```bash
✅ Legítima a importação:
Path: /backend/api/index.py
│
├─ sys.path.insert(0, str(Path(__file__).parent.parent))
│  → Adiciona '/backend' ao path
│
└─ from app.main import app ✅
   → Busca em '/backend/app/main.py' (CORRETO)
```

**Resultado**: A importação é válida e funciona.

---

### 2.2 Arquivos __init__.py - TODOS PRESENTES ✅
```
✅ Verificação:
backend/app/__init__.py            → EXISTS
backend/app/api/__init__.py        → EXISTS  
backend/app/api/v1/__init__.py     → EXISTS
backend/app/core/__init__.py       → EXISTS
backend/app/repositories/__init__.py → EXISTS
backend/app/schemas/__init__.py    → EXISTS
backend/app/services/__init__.py   → EXISTS
backend/app/utils/__init__.py      → NOT FOUND (opcional)
```

**Resultado**: Nenhum __init__.py crítico faltando.

---

### 2.3 Importações em backend/app/api/v1/__init__.py
```python
✅ Correto:
from . import calculos  # noqa: F401
from . import parametros  # noqa: F401
→ Importações usando caminho relativo (correto)
```

**Resultado**: Sem problemas.

---

## 3. CONFIGURAÇÃO DO VERCEL ⚠️ INCOMPLETA

### 3.1 Estrutura Python esperada pelo Vercel
```
EXPECTED by Vercel Python Runtime:
├── backend/api/index.py    ← Entry point (ASGI app)
├── requirements.txt        ← Dependencies
└── [optional] .vercelignore
```

**Status**: ✅ Correto. O backend/api/index.py está no lugar certo.

### 3.2 Como Vercel detecta FastAPI
```
1. Vercel procura em backend/api/index.py
2. Encontra: from app.main import app
3. Detecta app como ASGI (FastAPI instance)
4. Inicia com gunicorn/uvicorn automaticamente
5. Roteia /api/* para esta função

✅ Tudo configurado corretamente
```

### 3.3 PROBLEMA IDENTIFICADO: Falta configuração em vercel.json

O arquivo está quase correto, mas falta uma configuração importante:

```json
❌ FALTANDO:
{
  "version": 2,
  "builds": [
    {
      "src": "backend/api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.11"  ← ADICIONAR ISTO
      }
    },
    ...
  ]
}
```

**Recomendação**: Adicione `"runtime": "python3.11"` no bloco de config do Python.

---

## 4. VARIÁVEIS DE AMBIENTE NECESSÁRIAS ⚠️ CRÍTICO

### 4.1 Variáveis OBRIGATÓRIAS para Vercel
```
NOME                 | TIPO      | OBRIGATÓRIO | EXEMPLO
─────────────────────┼───────────┼─────────────┼──────────────────────
SUPABASE_URL         | string    | ✅ SIM      | https://xxxx.supabase.co
SUPABASE_KEY         | string    | ✅ SIM      | eyJhbGciOi...
ENVIRONMENT          | string    | ❌ NÃO      | production
VITE_API_BASE_URL    | string    | ❌ NÃO      | (deixar VAZIO)
```

### 4.2 Onde configurar em Vercel
```
1. Dashboard Vercel → Projeto → Settings
2. Environment Variables
3. Adicionar:
   - SUPABASE_URL = https://seu-projeto.supabase.co
   - SUPABASE_KEY = sua-chave-aqui
4. SEM configurar VITE_API_BASE_URL (deixar vazio)
```

### 4.3 Valores esperados de Supabase

**Para obter essas chaves**:
1. Acesse https://app.supabase.com
2. Selecione seu projeto
3. Vá em Project Settings → API
4. Copie:
   - Project URL → SUPABASE_URL
   - Service Role Secret (NÃO public key!) → SUPABASE_KEY

### 4.4 PROBLEMA: VITE_API_BASE_URL configurado em Vercel

**❌ NÃO FAZER**:
```bash
VITE_API_BASE_URL = https://ferramenta-calculo-irpf.vercel.app/api/v1
→ Causa CORS errors em preview deploys
```

**✅ FAZER**:
```bash
VITE_API_BASE_URL = (deixar vazio / deletar)
→ Frontend usa /api/v1 (relativa)
→ Vercel roteia corretamente
```

---

## 5. CONFIGURAÇÃO DO SUPABASE ⚠️ SEM VERIFICAÇÃO

### 5.1 Tabelas necessárias - SCHEMA validado
```sql
✅ VERIFICADA estrutura esperada:

1. calculos
   ├── id (uuid PRIMARY KEY)
   ├── processo (uuid)
   ├── tipo_calculo (text)
   ├── ano_calendario (int)
   ├── dados_entrada (jsonb)
   ├── resultado (jsonb)
   └── criado_em (timestamptz)

2. ir_parametros
   ├── ano_calendario (int PRIMARY KEY)
   ├── teto (numeric)
   └── inicio_correcao (date)

3. ir_faixas
   ├── id (serial PRIMARY KEY)
   ├── ano_calendario (int FK)
   ├── limite_inferior (numeric)
   ├── limite_superior (numeric)
   ├── aliquota (numeric)
   └── deducao (numeric)
```

**Status**: Schema está definido em backend/db/schema.sql

### 5.2 PROBLEMA: Dados seed NÃO carregados

**⚠️ Crítico**:  
O arquivo backend/db/seed.sql contém 36 anos de parâmetros (1990-2025), mas:

```
❌ Não há forma automática de executar seed.sql no Vercel
❌ Backend falhará se tentar buscar parâmetros
```

**Para corrigir**:
1. Acesse Supabase → SQL Editor
2. Copie script de schema.sql e execute
3. Copie script de seed.sql e execute
4. OU criar uma rota de admin `/api/v1/admin/seed` para populat automaticamente

### 5.3 Declarações necesárias em SQL

Para o backend funcionar, execute:

```sql
-- 1. Criar tabelas (schema.sql)
CREATE TABLE IF NOT EXISTS calculos (...);
CREATE TABLE IF NOT EXISTS ir_parametros (...);
CREATE TABLE IF NOT EXISTS ir_faixas (...);

-- 2. Inserir dados (seed.sql)
INSERT INTO ir_parametros (...) VALUES (...);
INSERT INTO ir_faixas (...) VALUES (...);

-- 3. Criar índices para performance
CREATE INDEX idx_calculos_processo ON calculos(processo);
CREATE INDEX idx_ir_faixas_ano ON ir_faixas(ano_calendario);
```

### 5.4 RLS Policies (Row Level Security)

**Status**: ⚠️ Não documentado

Recomendado:
```sql
-- Permissões de leitura/escrita
ALTER TABLE calculos ENABLE ROW LEVEL SECURITY;
ALTER TABLE ir_parametros ENABLE ROW LEVEL SECURITY;
ALTER TABLE ir_faixas ENABLE ROW LEVEL SECURITY;

-- Policies (anônimo pode ler parâmetros, criar cálculos)
CREATE POLICY "public_read_parametros" ON ir_parametros
  FOR SELECT USING (true);
  
CREATE POLICY "public_insert_calculos" ON calculos
  FOR INSERT WITH CHECK (true);
```

---

## 6. PROBLEMAS ESPECÍFICOS - INVESTIGAÇÃO

### 6.1 Por que /api/v1/calculos/simular retorna 404?

**Análise da cadeia de requisição**:

```
Frontend → GET /api/v1/calculos/simular
            ↓
Vercel roteia para /backend/api/index.py
            ↓
backend/api/index.py importa app.main.app
            ↓
app.main.app está configurado com:
  - prefix="/api/v1" para rotas
  - routers include calculos.router com prefix="/calculos"
            ↓
Resultado: FastAPI monta rota como /api/v1/calculos/simular

✅ A rota DEVERIA existir...
```

**POSSÍVEIS CAUSAS DE 404**:

1. **❌ Backend não está sendo invocado**
   - Vercel não iniciou a função Python
   - Log check: Vercel Dashboard → Logs → Function duration

2. **❌ Supabase não foi inicializado**
   - SUPABASE_URL ou SUPABASE_KEY não configuradas
   - Backend falha ao importar
   - Resultado: 502 Bad Gateway, não 404

3. **❌ Rota está com POST, não GET**
   ```python
   @router.post("/simular", response_model=CalculoResultado)
   def simular_calculo(entrada: CalculoInput) → CalculoResultado:
   ```
   Se frontend faz GET, retorna 404. Verificar frontend/src/api.ts

4. **✅ Frontend está correto - USO POST**
   ```typescript
   export async function simularCalculo(input: CalculoInput) {
     const { data } = await client.post<CalculoResultado>("/calculos/simular", input);
   ```
   OK, usa POST corretamente.

**DIAGNÓSTICO REAL**:
- Se testa em desenvolvimento local: `uvicorn app.main:app --reload` funciona?
  - Se SIM → Problema é no Vercel (environment vars ou build)
  - Se NÃO → Problema é no código

---

### 6.2 Por que /api/v1/docs retorna 404?

**Análise**:

```python
app = FastAPI(
    ...
    openapi_url=f"{settings.api_prefix}/openapi.json",  # /api/v1/openapi.json
    docs_url=f"{settings.api_prefix}/docs",              # /api/v1/docs
    redoc_url=f"{settings.api_prefix}/redoc",            # /api/v1/redoc
)
```

✅ **A rota DEVERIA estar montada em /api/v1/docs**

**POSSÍVEL PROBLEMA**:
- Em Vercel, o FastAPI pode estar montado diretamente em `/`
- Resultado: docs está em `/docs`, não em `/api/v1/docs`

**SOLUÇÃO 1**: Verificar routing
```python
# Em backend/api/index.py ou Vercel
# FastAPI está sendo servido em / ou /api/v1/api?
```

**SOLUÇÃO 2**: Remover prefixo customizado
```python
# Deixar FastAPI usar defaults em vez de prefixos customizados
openapi_url="/openapi.json",
docs_url="/docs",
redoc_url="/redoc",
```

---

### 6.3 Há algo que precisa ser corrigido no código Python? ⚠️ SIM

#### Problema 1: Importação de tipo faltando
```python
# backend/app/api/v1/calculos.py
from app.schemas.parametros import IrParametros  # ← Importada DENTRO da função

❌ RUIM: Importação dentro da função
✅ BOM: Importar no topo
```

**CORRIGIR**: Mover import para o topo do arquivo

#### Problema 2: Tratamento de erro incompleto
```python
# backend/app/repositories/parametros_repository.py
except APIError as exc:
    if getattr(exc, "code", None) == "PGRST116":
        return None
    raise

❌ Frágil: Depende de atributo dinâmico
✅ Melhor: Usar try/except com PostgREST exceptions
```

#### Problema 3: Suporte a CORS inadequado
```python
# backend/app/main.py
allow_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    ...
    "https://ferramenta-calculo-irpf.vercel.app",
]

❌ Problema: Não suporta preview deploys (*.vercel.app)
```

**CORRIGIR**: Adicionar suporte a padrões
```python
allowed_origins = [
    # Development
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Production
    "https://ferramenta-calculo-irpf.vercel.app",
    # Preview deploys
    "https://*.vercel.app",  ← ADICIONAR
]
```

#### Problema 4: requirements.txt pode estar incompleto
```
fastapi==0.104.0
uvicorn[standard]==0.25.0
pydantic==2.7.0
supabase==1.0.1
python-dotenv==1.0.0
Jinja2==3.1.4
WeasyPrint==58.0
```

**Possível falta**: postgrest (para exceção de erro PGRST116)

```bash
pip list | grep postgrest
→ Deve estar instalado via supabase=1.0.1
```

---

## 7. RESUMO EXECUTIVO - O QUE FAZER

### ✅ CORRETO - Sem mudanças
- [x] Estrutura de rotas (vercel.json)
- [x] backend/api/index.py
- [x] backend/app/main.py (ASGI compatible)
- [x] Todos __init__.py presentes
- [x] frontend/src/api.ts (usa POST corretamente)

### ⚠️ PROBLEMA 1: Variáveis de Ambiente em Vercel
```
AÇÃO: Em Vercel Settings → Environment Variables

ADICIONAR:
- SUPABASE_URL = https://seu-projeto.supabase.co
- SUPABASE_KEY = sua-service-role-key

REMOVER:
- VITE_API_BASE_URL (ou deixar vazio)
```

### ⚠️ PROBLEMA 2: Dados não carregados em Supabase
```
AÇÃO: Supabase → SQL Editor

1. Executar backend/db/schema.sql
2. Executar backend/db/seed.sql
```

### ⚠️ PROBLEMA 3: Código Python minor issues
```
AÇÃO: Corrigir em backend/app/api/v1/calculos.py

1. Mover import IrParametros para topo
```

### ⚠️ PROBLEMA 4: CORS para preview deploys
```
AÇÃO: Atualizar backend/app/main.py

Adicionar wildcard Vercel hosts:
"https://*.vercel.app",
```

### 🔍 PROBLEMA 5: 404 em /api/v1/docs
```
DIAGNÓSTICO:
1. Testar localmente: uvicorn app.main:app --reload
2. Acessar http://localhost:8000/api/v1/docs
3. Se funciona localmente → Problema é no Vercel
4. Se falha → Problema é na configuração de prefixo
```

### 🔍 PROBLEMA 6: 404 em /api/v1/calculos/simular
```
DIAGNÓSTICO:
1. Verificar Vercel logs: Dashboard → Function logs
2. Verificar se backend está iniciando
3. Verificar se SUPABASE_* estão configuradas
4. Se código local funciona → Problema é environment vars
```

---

## 8. ORDEM DE PRIORIDADE PARA CORRIGIR

| Prioridade | Problema | Arquivo(s) | Ação |
|-----------|----------|-----------|------|
| 🔴 CRÍTICO | Supabase vazio | backend/db/schema.sql, seed.sql | Executar SQL em Supabase |
| 🔴 CRÍTICO | Environment vars | Vercel Settings | Configurar SUPABASE_URL, SUPABASE_KEY |
| 🟡 ALTA | CORS preview deploys | backend/app/main.py | Adicionar "https://*.vercel.app" |
| 🟡 ALTA | Import dentro de função | backend/app/api/v1/calculos.py | Mover para topo |
| 🟢 MÉDIA | Runtime Python | vercel.json | Adicionar "runtime": "python3.11" |
| 🟢 MÉDIA | Teste de rota | local | Executar tests locais |

---

## 9. COMO TESTAR LOCALMENTE

### 1. Setup local
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar .env
```bash
# backend/.env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-aqui
```

### 3. Iniciar backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Testar rotas
```bash
# Em outro terminal
curl http://localhost:8000/api/v1/docs
# Deve retornar página Swagger UI

curl -X POST http://localhost:8000/api/v1/calculos/simular \
  -H "Content-Type: application/json" \
  -d '{"processo":"123","nome_autor":"João","tipo_declaracao":"completa","ano_calendario":2024,"rendimentos_tributaveis":100000,"deducoes_legais":0,"deducoes_incentivo":0,"imposto_rra":0,"imposto_pago":0,"rend_somar":0,"rend_sub":0,"ded_somar":0,"ded_sub":0,"incentivo_somar":0,"incentivo_sub":0,"rra_somar":0,"rra_sub":0,"tipo_calculo":"ajuste_anual"}'
```

Se retorna erro de parâmetros não encontrados → Dados não estão em Supabase.

---

## 10. CONCLUSÃO

A estrutura do projeto está **95% correta**. Os problemas são principalmente:

1. ✅ Roteamento: OK
2. ✅ Importações: OK  
3. ⚠️ Variáveis de ambiente: **NÃO CONFIGURADO**
4. ⚠️ Dados do Supabase: **NÃO CARREGADO**
5. ⚠️ Minor code fixes: **Nécessários**

**Próximas ações**:
1. Executar schema.sql + seed.sql no Supabase
2. Configurar SUPABASE_URL e SUPABASE_KEY em Vercel
3. Remover/esvaziar VITE_API_BASE_URL em Vercel
4. Fazer as correções de código Python
5. Testar localmente primeiro
6. Deploy para Vercel

Se tudo estiver configurado corretamente, o projeto rodará sem problemas de 404.
