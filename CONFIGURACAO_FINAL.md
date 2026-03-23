# ⚙️ CONFIGURAÇÃO DO PROJETO - Checklist Completo

## 🔴 PROBLEMAS IDENTIFICADOS

O erro **404** não é de roteamento, mas de **Supabase não inicializado** e **variáveis de ambiente ausentes no Vercel**.

Quando a aplicação tenta acessar `/api/v1/calculos/simular`:
1. FastAPI tenta carregar a config via `config.py`
2. Config precisa de `SUPABASE_URL` e `SUPABASE_KEY`
3. Sem estas variáveis, a app falha ao iniciar
4. Vercel retorna 502/timeout que aparece como 404

---

## ✅ PASSO 1: Configurar Supabase (10 minutos)

### 1.1 Criar Tabelas

Acesse: **https://app.supabase.com** → Seu Projeto → SQL Editor

**Execute Script 1: Schema**
```sql
-- Cole todo o conteúdo de: backend/db/schema.sql
-- Cria as 3 tabelas: calculos, ir_parametros, ir_faixas
```

**Execute Script 2: Dados**
```sql
-- Cole todo o conteúdo de: backend/db/seed.sql
-- Popula ir_parametros com anos 1990-2025
-- Popula ir_faixas com as alíquotas de cada ano
```

### 1.2 Obter Credenciais

Supabase → **Settings** → **API**

Copie:
- **Project URL** → será `SUPABASE_URL`
- **Service Role Secret** → será `SUPABASE_KEY`

```
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## ✅ PASSO 2: Configurar Vercel Environment Variables (5 minutos)

### 2.1 Acessar Settings

Vercel → Seu Projeto → **Settings** → **Environment Variables**

### 2.2 REMOVER (Altamente Importante!)

Se existir, **DELETE ou deixe vazio:**
```
VITE_API_BASE_URL
```

Isto causa CORS errors porque força URL absoluta em preview deploys.

### 2.3 ADICIONAR Variáveis do Backend

```
Name: SUPABASE_URL
Value: https://seu-projeto.supabase.co

Name: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (chave completa)
```

✅ **Available in**: Selecionar `Production` e `Preview` ou deixar `All`

### 2.4 Salvar

Clique em "Save"

⚠️ **IMPORTANTE**: O Vercel **redeploy automaticamente** após salvar variáveis

---

## ✅ PASSO 3: Testar Funcionalidade (5 minutos)

### 3.1 Verificar API Docs

```
https://ferramenta-calculo-irpf.vercel.app/api/v1/docs
```

Deve carregar sem 404.

### 3.2 Testar Simulação via cURL

```bash
curl -X POST "https://ferramenta-calculo-irpf.vercel.app/api/v1/calculos/simular" \
  -H "Content-Type: application/json" \
  -d '{
    "processo": "2025000001",
    "nome_autor": "Teste",
    "tipo_declaracao": "completa",
    "ano_calendario": 2024,
    "rendimentos_tributaveis": 100000,
    "deducoes_legais": 5000,
    "imposto_pago": 15000,
    "tipo_calculo": "ajuste_anual"
  }'
```

Deve retornar JSON com resultado do cálculo.

### 3.3 Testar Frontend

```
https://ferramenta-calculo-irpf.vercel.app/calculo/ajuste-anual
```

Preencher formulário e clicar "Simular" deve funcionar.

---

## ✅ PASSO 4: Testar Localmente (Opcional, para Desenvolvimento)

Se quiser testar localmente antes de fazer push:

### 4.1 Criar arquivo `.env`

```bash
cd backend
```

Criar arquivo `.env`:
```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-aqui
```

### 4.2 Instalar Dependências

```bash
py -m pip install -r requirements.txt
```

### 4.3 Executar Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4.4 Executar Frontend (em outro terminal)

```bash
cd frontend
npm install
npm run dev
```

Acessar: `http://localhost:5173`

---

## 📋 Estrutura Final Esperada

```
backend/
├── api/
│   └── index.py (handler Vercel)
├── app/
│   ├── main.py (FastAPI app + CORS)
│   ├── api/v1/
│   │   ├── calculos.py (rotas /calculos)
│   │   └── parametros.py (rotas /parametros)
│   ├── services/ (lógica de cálculo)
│   ├── repositories/ (acesso a dados)
│   └── core/
│       ├── config.py (env vars)
│       └── supabase.py (cliente)
├── db/
│   ├── schema.sql ✅ EXECUTADO
│   └── seed.sql ✅ EXECUTADO
├── requirements.txt
├── .env ✅ Configurado locally
└── index.py (antigo, pode deletar)

frontend/
├── vite.config.ts (proxy local)
├── .env.example (documentação)
└── src/
    ├── api.ts (URL relativa /api/v1)
    └── pages/

vercel.json ✅ Correto
```

---

## 🔍 Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `/api/v1/docs` → 404 | Supabase vazio ou env vars não carregadas | Executar schema.sql + seed.sql em Supabase |
| `/api/v1/calculos/simular` → 404 | Idem | Idem |
| CORS Error | `VITE_API_BASE_URL` definida em Vercel | Remover ou deixar vazio essa variável |
| Simular retorna 500 | Parâmetros do ano não existem | Verificar seed.sql tem dados para 2024/2025 |
| Frontend em branco | CORS ou fetch error | Abrir DevTools console e checar erro exato |

---

## ✨ Resumo Executivo

```
O QUE FAZER:
1. Supabase SQL Editor: Executar 2 scripts (schema.sql + seed.sql)
2. Vercel Settings: Adicionar SUPABASE_URL e SUPABASE_KEY
3. Vercel Settings: REMOVER VITE_API_BASE_URL (vazio)
4. Aguardar redeploy automático (~5 min)
5. Testar em https://seu-projeto.vercel.app

CÓDIGO: Já está corrigido ✅
```

---

## 📞 Checklist Final

- [ ] Schema.sql executado em Supabase
- [ ] Seed.sql executado em Supabase (veja se ir_parametros tem 2024/2025)
- [ ] SUPABASE_URL adicionada em Vercel
- [ ] SUPABASE_KEY adicionada em Vercel
- [ ] VITE_API_BASE_URL removida/vazia em Vercel
- [ ] Vercel redeploy completou (status ✅)
- [ ] `/api/v1/docs` carrega sem 404
- [ ] Simulação retorna resultado JSON
- [ ] Frontend clica em "Simular" e funciona

Assim que completar, sua ferramenta estará **100% funcional**! 🎉
