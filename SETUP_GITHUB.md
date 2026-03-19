# Setup no GitHub e Vercel

## Instruções para vincular ao GitHub

### Passo 1: Criar repositório no GitHub

1. Acesse https://github.com/new
2. Preencha os dados:
   - **Repository name**: `ferramenta-calculo-irpf` (ou outro nome de sua preferência)
   - **Description**: "Ferramenta de cálculo de ajuste anual e retificação de IRPF"
   - **Visibility**: Public (recomendado para Vercel) ou Private
   - **NÃO** initialize com README, .gitignore ou licença (já temos)
3. Clique em "Create repository"

### Passo 2: Adicionar origin remoto e fazer push

Após criar o repositório, copie o URL HTTPS (ex: `https://github.com/contaagoijf/ferramenta-calculo-irpf.git`) e execute:

```bash
cd c:\Users\c4c\Desktop\Projetos\ferramenta-calculo-irpf

# Adicionar origem remota (substitua pela URL do seu repositório)
git remote add origin https://github.com/contaagoijf/ferramenta-calculo-irpf.git

# Verificar se a origem foi adicionada
git remote -v

# Fazer push da branch main
git branch -M main
git push -u origin main
```

Se pedir autenticação, use:
- **Username**: seu login do GitHub
- **Password**: seu Personal Access Token (PAT)

> 💡 Se não tiver um PAT, crie em: https://github.com/settings/tokens

### Passo 3: Configurar deploy no Vercel

1. Acesse https://vercel.com e faça login (ou crie conta) com GitHub
2. Clique em "Add New" → "Project"
3. Selecione o repositório `ferramenta-calculo-irpf`
4. Configure:
   - **Framework Preset**: Next.js (ou Other se usar Vite)
   - **Root Directory**: `./frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Adicione variáveis de ambiente (se necessário):
   - `VITE_API_BASE_URL`: URL da sua API (ex: `https://seu-backend.com/api/v1`)
6. Clique em "Deploy"

### Passo 4: Deploy do backend (Supabase / Railway / Render)

Para o backend FastAPI, você pode usar:

**Opção A: Supabase + Edge Functions**
- Não suportado nativamente; use Railway ou Render

**Opção B: Railway (recomendado)**
1. Acesse https://railway.app
2. Crie novo projeto
3. Conecte seu GitHub
4. Configure para rodar:
   ```
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

**Opção C: Render**
1. Acesse https://render.com
2. Novo "Web Service"
3. Conecte seu GitHub
4. Configure `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

## Estrutura esperada no GitHub

```
ferramenta-calculo-irpf/
├── .gitignore
├── README.md
├── SETUP_GITHUB.md (este arquivo)
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py
│   │   ├── api/v1/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── ...
│   └── db/
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── src/
│   └── ...
└── extract_pdf.py
```

## Próximos passos

✅ Backend deployado
✅ Frontend deployado no Vercel
✅ Supabase configurado com tabelas
✅ Variáveis de ambiente definidas (.env no backend, VITE_* no Vercel)

---

Dúvidas? Verifique os logs de deploy em:
- Vercel: https://vercel.com/dashboard
- Railway/Render: painel respectivo
