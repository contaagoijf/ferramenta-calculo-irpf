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
   - **Framework Preset**: Other
   - **Root Directory**: `./` (raiz do projeto)
   - **Build Command**: Deixar em branco (Vercel detecta automaticamente)
   - **Output Directory**: `frontend/dist`
5. **Variáveis de ambiente** (IMPORTANTE):
   - **NÃO configure** `VITE_API_BASE_URL` - deixe vazio para usar URLs relativas
   - Configure as variáveis do backend:
     - `SUPABASE_URL`: URL do seu projeto Supabase
     - `SUPABASE_KEY`: Chave de acesso do Supabase
6. Clique em "Deploy"

**Nota Importante**: O Vercel automaticamente roteia `/api/*` para o backend FastAPI e `/*` para o frontend React, ambos no mesmo domínio. URLs relativas `/api/v1` funcionam perfeitamente em produção.

### Passo 4: Após Deploy

Após o deploy ser concluído:

1. Acesse a URL gerada pelo Vercel (ex: `https://ferramenta-calculo-irpf.vercel.app`)
2. A aplicação estará rodando com:
   - Frontend React em Vite servido em `/`
   - Backend FastAPI servido em `/api/v1/`
3. Consulte a documentação interativa da API em `/api/v1/docs`

**Troubleshooting**:
- Se receber erros de CORS, verifique se `VITE_API_BASE_URL` está vazio no Vercel
- Se a API retornar 404, verifique se `SUPABASE_URL` e `SUPABASE_KEY` estão configuradas
- Para preview deploys, a mesma configuração funciona automaticamente

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
