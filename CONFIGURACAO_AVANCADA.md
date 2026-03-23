# 🔐 Configurações Avançadas - Supabase & Vercel

## SUPABASE - Configurações Especiais

### Row Level Security (RLS)

Se você habilitou RLS (Row Level Security) no Supabase, adicione estas políticas:

#### Tabela `calculos`

```sql
-- Política para INSERT (qualquer um pode criar)
CREATE POLICY "Permitir inserção de calculos"
ON public.calculos FOR INSERT
WITH CHECK (true);

-- Política para SELECT (qualquer um pode ler)
CREATE POLICY "Permitir leitura de calculos"
ON public.calculos FOR SELECT
USING (true);

-- Política para UPDATE (proprietário pode atualizar)
CREATE POLICY "Atualizar cálculos próprios"
ON public.calculos FOR UPDATE
USING (auth.uid()::text = processo::text) -- ou sua lógica
WITH CHECK (true);
```

#### Tabela `ir_parametros`

```sql
-- Política para SELECT (público)
CREATE POLICY "Permitir leitura de parametros"
ON public.ir_parametros FOR SELECT
USING (true);
```

#### Tabela `ir_faixas`

```sql
-- Política para SELECT (público)
CREATE POLICY "Permitir leitura de faixas"
ON public.ir_faixas FOR SELECT
USING (true);
```

**Para Habilitar RLS:**
1. Supabase Dashboard → Authentication → Policies
2. Para cada tabela, ativar "RLS" toggle
3. Adicionar políticas acima

**Ou deixe RLS desativado** para desenvolvimento/MVP (menos seguro, mas mais simples).

---

## Chaves Supabase - Qual Usar?

| Tipo de Chave | Uso | Quando Usar |
|---------------|-----|------------|
| `anon` (Publicable) | Frontend | ❌ NÃO use no backend |
| `service_role` (Secret) | Backend | ✅ USE no Vercel (SUPABASE_KEY) |

**Você deve usar: `service_role` (chave Secret)**

Esta é a chave que dá permissão de admin no Supabase, segura no backend do Vercel.

---

## VERCEL - Todas as Variáveis (Completo)

### Required Environment Variables

```
# Backend - Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (service_role)
```

### Optional (NÃO definir, deixar vazio ou remover)

```
VITE_API_BASE_URL=   # ← DEIXAR VAZIO (usa /api/v1 relativa)
```

### Default (automático, não precisa definir)

- `PYTHON_VERSION=3.11` (automaticamente detectado)
- `NODE_VERSION=18` (automaticamente detectado)

---

## Domínios Permitidos

O projeto funciona em:
- ✅ `https://ferramenta-calculo-irpf.vercel.app` (produção)
- ✅ `https://ferramenta-calculo-irpf-*.vercel.app` (preview deploys)
- ✅ `http://localhost:3000` (desenvolvimento)
- ✅ `http://localhost:5173` (desenvolvimento)
- ✅ `http://127.0.0.1:*` (desenvolvimento)

---

## Build & Runtime Specifications

### Frontend
- **Framework**: React 18 + Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Backend
- **Runtime**: `python3.11`
- **Framework**: FastAPI
- **Server**: Uvicorn (via Vercel Python build)
- **Build Command**: `pip install -r requirements.txt`

---

## Banco de Dados - Supabase Specs

### Tabelas Obrigatórias

1. **`ir_parametros`**
   - `ano_calendario` (int) - PK
   - `teto` (numeric)
   - `inicio_correcao` (date)

2. **`ir_faixas`**
   - `id` (serial) - PK
   - `ano_calendario` (int) - FK
   - `limite_inferior` (numeric)
   - `limite_superior` (numeric)
   - `aliquota` (numeric)
   - `deducao` (numeric)

3. **`calculos`**
   - `id` (uuid) - PK
   - `processo` (uuid)
   - `tipo_calculo` (text)
   - `ano_calendario` (int)
   - `dados_entrada` (jsonb)
   - `resultado` (jsonb)
   - `criado_em` (timestamptz)

### Seed Data Necessário

Mínimo: Dados de pelo menos um ano (recomendado 2024-2025)

O arquivo `backend/db/seed.sql` tem todos os anos 1990-2025.

---

## Performance & Limits

### Supabase Gratuito
- 500 MB storage
- 2 GB bandwidth/mês
- Rate limit: 1000 req/min

### Vercel Gratuito
- 10 GB bandwidth/mês
- 1000 serverless function invocations/mês
- Builds ilimitados

Para MVP, tudo funciona no gratuito! 🎉

---

## Segurança Checklist

- [ ] Usar `service_role` key em Vercel (não `anon`)
- [ ] Não commitar `.env` com credenciais (já no `.gitignore`)
- [ ] Habilitar RLS no Supabase em produção
- [ ] Adicionar políticas de acesso apropriadas
- [ ] HTTPS apenas (Vercel automático)
- [ ] Validar inputs no backend (Pydantic ✅)

---

## Monitoramento

### Vercel Logs
```
Vercel → Seu Projeto → Deployments → Ver Logs
```

Procure por:
- `ERROR` ou `500 Internal Server Error`
- Imports falhando
- Variáveis de ambiente não encontradas

### Supabase Logs
```
Supabase → Settings → Logs
```

Procure por:
- Queries falhando
- Auth errors
- RLS violações

---

## URLs Úteis

| Recurso | Link |
|---------|------|
| Seu Projeto Vercel | https://vercel.com/dashboard |
| Seu Projeto Supabase | https://app.supabase.com |
| API Docs | `https://seu-projeto.vercel.app/api/v1/docs` |
| Redoc | `https://seu-projeto.vercel.app/api/v1/redoc` |

---

Qualquer dúvida, verifique os logs em Vercel ou Supabase!
