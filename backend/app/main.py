from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import calculos, parametros
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ferramenta de Cálculo IRPF",
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    # Configurar CORS com suporte a origens múltiplas
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",  # Em produção, considere ser mais específico
        ],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=600,
    )

    app.include_router(calculos.router, prefix=settings.api_prefix)
    app.include_router(parametros.router, prefix=settings.api_prefix)

    return app


app = create_app()
