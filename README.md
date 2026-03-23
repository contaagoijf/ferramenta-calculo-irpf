# Ferramenta de Cálculo IRPF

Ferramenta MVP para cálculo de ajuste anual/retificação de IRPF, com backend em FastAPI, banco Supabase e frontend em React.

## Estrutura

- `backend/`: API em FastAPI com validação Pydantic e persistência no Supabase.
- `frontend/`: Aplicação React (Vite) consumindo os endpoints via proxy.
- `backend/db/`: Scripts de criação e seed das tabelas.

## Como começar

### Backend (FastAPI)

1. Crie um arquivo `.env` em `backend/` com variáveis:

```env
SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_KEY=<sua-service-role-key>
ENVIRONMENT=development
```

2. Instale dependências e execute:

```sh
cd backend
py -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Acesse a documentação interativa em: `http://localhost:8000/api/v1/docs`

### Frontend (React)

1. Configure variáveis de ambiente (opcional em desenvolvimento):

```sh
cd frontend
cp .env.example .env.local
# Deixe VITE_API_BASE_URL vazio para usar proxy local
```

2. Instale e execute:

```sh
npm install
npm run dev
```

Acesse: `http://localhost:5173`

**Nota**: Em desenvolvimento, o Vite proxy (`vite.config.ts`) redireciona `/api/*` para `http://localhost:8000/api/*` automaticamente.

## Configuração para Produção (Vercel)

1. **Environment Variables** no painel Vercel:
   - Adicionar variáveis do backend em `backend/` settings
   - `SUPABASE_URL` - URL do seu projeto Supabase
   - `SUPABASE_KEY` - Chave de acesso do Supabase
   - `ENVIRONMENT` - Definir como `production`

2. **Routing** (automático via `vercel.json`):
   - `/api/*` → Backend Python
   - `/*` → Frontend React (SPA com fallback)

3. **CORS**:
   - Backend aceita: `https://ferramenta-calculo-irpf.vercel.app` e `https://*.vercel.app`
   - Frontend usa URLs relativas `/api/v1` (roteado através do Vercel)

## Fluxo principal

1. **Simular** → chama `/api/v1/calculos/simular` (backend).
2. **Finalizar** → cria registro em Supabase via `/api/v1/calculos`.
3. **Relatório** → consulta por ID e gera PDF via `/api/v1/calculos/{id}/pdf`.

## Observações

- O cálculo de retificação implementa a mesma lógica do ajuste anual como placeholder.
- Todos os cálculos são determinísticos e baseados em `Decimal`.
- A geração de PDF usa `WeasyPrint` a partir de template HTML (`backend/app/templates/relatorio.html`).
- Em desenvolvimento, o proxy Vite resolve automaticamente requisições `/api` para a porta 8000
- Em produção, o Vercel roteia `/api` para a função Python serverless
