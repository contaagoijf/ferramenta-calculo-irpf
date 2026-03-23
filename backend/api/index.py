"""
Vercel Serverless Function Handler para FastAPI
Este arquivo é o entry point para o Vercel como função serverless
"""
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar 'app'
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Vercel espera uma função handler ou uma app ASGI
# Exportando a app FastAPI para que o Vercel a detecte como ASGI
# O Vercel passará as requisições HTTP para esta aplicação
__all__ = ["app"]
