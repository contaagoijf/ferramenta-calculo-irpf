# CORREÇÕES DE CÓDIGO NECESSÁRIAS

## 1. Correção em backend/app/api/v1/calculos.py
**Problema**: Import de `IrParametros` está dentro da função (line 29)  
**Impacto**: Ineficiência, dificulta type checking estático  
**Solução**: Mover import para topo do arquivo

### Antes:
```python
from app.repositories.calculo_repository import fetch_calculo_by_id, insert_calculo
from app.repositories.parametros_repository import fetch_parametros
from app.schemas.calculo import CalculoCreate, CalculoInput, CalculoInDB, CalculoResultado, TipoCalculo
from app.services.calculo_service import calcular_ajuste_anual, calcular_retificacao
from app.utils.pdf import render_relatorio_pdf

router = APIRouter(prefix="/calculos", tags=["calculos"])


@router.post("/simular", response_model=CalculoResultado)
def simular_calculo(entrada: CalculoInput) -> CalculoResultado:
    parametros_dict = fetch_parametros(entrada.ano_calendario)
    if not parametros_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parâmetros de IR não encontrados para o ano informado.",
        )

    from app.schemas.parametros import IrParametros  # ← AQUI (RUIM)

    parametros = IrParametros(**parametros_dict)
```

### Depois:
```python
from app.repositories.calculo_repository import fetch_calculo_by_id, insert_calculo
from app.repositories.parametros_repository import fetch_parametros
from app.schemas.calculo import CalculoCreate, CalculoInput, CalculoInDB, CalculoResultado, TipoCalculo
from app.schemas.parametros import IrParametros  # ← ADICIONADO AQUI (BOM)
from app.services.calculo_service import calcular_ajuste_anual, calcular_retificacao
from app.utils.pdf import render_relatorio_pdf

router = APIRouter(prefix="/calculos", tags=["calculos"])


@router.post("/simular", response_model=CalculoResultado)
def simular_calculo(entrada: CalculoInput) -> CalculoResultado:
    parametros_dict = fetch_parametros(entrada.ano_calendario)
    if not parametros_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parâmetros de IR não encontrados para o ano informado.",
        )

    parametros = IrParametros(**parametros_dict)  # ← Removido import daqui
```

---

## 2. Correção em backend/app/main.py
**Problema**: CORS permite hardcoded origins, mas não *.vercel.app  
**Impacto**: Preview deploys do Vercel recebem erro CORS  
**Solução**: Adicionar wildcard suporte para Vercel preview URLs

### Antes:
```python
allowed_origins = [
    # Development environments
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Production
    "https://ferramenta-calculo-irpf.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ← Lista estática
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)
```

### Depois:
```python
def _is_allowed_origin(origin: str) -> bool:
    """Check if origin is allowed for CORS."""
    # Development
    if origin in [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]:
        return True
    
    # Production
    if origin == "https://ferramenta-calculo-irpf.vercel.app":
        return True
    
    # Vercel preview deploys
    if origin.endswith(".vercel.app"):
        return True
    
    return False


# Configure CORS with dynamic origin checking
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|.*\.vercel\.app):?\d*",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)
```

**OU (mais simples)**:
```python
# Se prefere manter lista explícita com padrões
from fastapi.middleware.cors import CORSMiddleware

# Para desenvolvimento e preview, pode usar allow_origins com ['*']
# JÁ QUE as rotas devem estar no mesmo domínio em produção

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Development
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # Production and previews
        "https://ferramenta-calculo-irpf.vercel.app",
        "https://*.vercel.app",  # ← Aceita todos os subdomínios .vercel.app
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)
```

**Nota**: FastAPI com CORSMiddleware aceita strings com `*` em padrões.

---

## 3. Atualização em vercel.json
**Problema**: Não especifica Python runtime  
**Impacto**: Vercel pode usar versão padrão (pode não ser Python 3.11)  
**Solução**: Adicionar runtime apropriado

### Antes:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/api/index.py",
      "use": "@vercel/python"
    },
```

### Depois:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/api/index.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.11"
      }
    },
```

---

## 4. Adição em backend/requirements.txt
**Problema**: Algumas dependencies podem estar faltando  
**Impacto**: Runtime errors em Vercel  
**Solução**: Adicionar packages explícitos se necessário

### Verificar:
```
pip list | grep postgrest
pip list | grep python-multipart
```

### Se faltam, adicione:
```
fastapi==0.104.0
uvicorn[standard]==0.25.0
pydantic==2.7.0
pydantic-settings==2.1.0  # ← Adicionar se usando pydantic v2
supabase==1.0.1
python-dotenv==1.0.0
Jinja2==3.1.4
WeasyPrint==58.0
python-multipart==0.0.6  # ← Para form data no FastAPI
```

---

## IMPLEMENTAÇÃO (ORDEM DE PRIORIDADE)

### 1. **IMEDIATAMENTE** - Dados em Supabase
```sql
-- Acessar Supabase → SQL Editor e executar:
-- backend/db/schema.sql
-- backend/db/seed.sql
```

### 2. **IMEDIATAMENTE** - Environment em Vercel
```
Vercel Dashboard → Projeto → Settings → Environment Variables

Adicionar:
SUPABASE_URL = https://seu-projeto.supabase.co
SUPABASE_KEY = sua-chave-aqui

Remover ou deixar vazio:
VITE_API_BASE_URL
```

### 3. **HOJE** - Correções de Código
- [ ] Mover import em calculos.py
- [ ] Atualizar CORS em main.py
- [ ] Atualizar vercel.json com runtime

### 4. **HOJE** - Teste Local
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Criar backend/.env com credenciais Supabase
echo "SUPABASE_URL=..." > .env
echo "SUPABASE_KEY=..." >> .env

# Testar
uvicorn app.main:app --reload --port 8000

# Em outro terminal
curl -X POST http://localhost:8000/api/v1/calculos/simular \
  -H "Content-Type: application/json" \
  -d '{"processo":"123","nome_autor":"João","tipo_declaracao":"completa","ano_calendario":2024,"rendimentos_tributaveis":100000, ...}'
```

### 5. **Dia seguinte** - Deploy
```bash
git add .
git commit -m "Fix: import, cors, vercel runtime"
git push origin main
# Vercel faz deploy automaticamente
```

---

## CHECKLIST DE VALIDAÇÃO

Antes de considerar "PRONTO":

- [ ] Schema.sql executado (3 tabelas criadas)
- [ ] Seed.sql executado (36 anos de parâmetros)
- [ ] SUPABASE_URL configurada em Vercel
- [ ] SUPABASE_KEY configurada em Vercel
- [ ] VITE_API_BASE_URL vazio/removido em Vercel
- [ ] calculos.py import corrigido
- [ ] main.py CORS atualizado
- [ ] vercel.json com runtime
- [ ] Teste local: `POST /api/v1/calculos/simular` retorna resultado
- [ ] Teste local: `GET /api/v1/docs` retorna Swagger UI
- [ ] Teste em produção: `/api/v1/docs` carrega no Vercel
- [ ] Teste em produção: simular cálculo funciona
- [ ] Preview deploy funciona sem CORS errors
