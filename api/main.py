from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import calculos, parametros
from .core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ferramenta de Cálculo IRPF",
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(calculos.router, prefix=settings.api_prefix)
    app.include_router(parametros.router, prefix=settings.api_prefix)

    return app


app = create_app()</content>
<parameter name="filePath">c:/Users/c4c/Documents/ferramenta-calculo-irpf/api/main.py