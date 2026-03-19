# Ferramenta de Cálculo IRPF

Ferramenta MVP para cálculo de ajuste anual/retificação de IRPF, com backend em FastAPI, banco Supabase e frontend em React.

## Estrutura

- `backend/`: API em FastAPI com validação Pydantic e persistência no Supabase.
- `frontend/`: Aplicação React (Vite) consumindo os endpoints.
- `backend/db/`: Scripts de criação e seed das tabelas.

## Como começar

### Backend (FastAPI)

1. Crie um arquivo `.env` em `backend/` com variáveis:

```env
SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_KEY=<sua-service-role-key>
```

2. Instale dependências e execute:

```sh
cd backend
py -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Acesse a documentação interativa em: `http://localhost:8000/api/v1/docs`

### Frontend (React)

```sh
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:5173`

## Fluxo principal

1. **Simular** → chama `/api/v1/calculos/simular` (backend).
2. **Finalizar** → cria registro em Supabase via `/api/v1/calculos`.
3. **Relatório** → consulta por ID e gera PDF via `/api/v1/calculos/{id}/pdf`.

## Observações

- O cálculo de retificação implementa a mesma lógica do ajuste anual como placeholder.
- Todos os cálculos são determinísticos e baseados em `Decimal`.
- A geração de PDF usa `WeasyPrint` a partir de template HTML (`backend/app/templates/relatorio.html`).
