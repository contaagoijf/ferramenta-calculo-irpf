from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.repositories.parametros_repository import (
    fetch_parametros,
    upsert_faixas,
    upsert_parametros,
)
from app.schemas.parametros import IrFaixa, IrParametros

router = APIRouter(prefix="/parametros", tags=["parametros"])


@router.get("/{ano_calendario}", response_model=IrParametros)
def obter_parametros(ano_calendario: int) -> IrParametros:
    record = fetch_parametros(ano_calendario)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parâmetros não encontrados")
    return IrParametros(**record)


@router.put("/{ano_calendario}", response_model=IrParametros)
def atualizar_parametros(ano_calendario: int, parametros: IrParametros) -> IrParametros:
    if parametros.ano_calendario != ano_calendario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O ano de calendário da URL e do payload devem ser iguais.",
        )

    saved = upsert_parametros(parametros.dict(exclude={"faixas"}))
    # salva faixas separadamente
    if parametros.faixas:
        upsert_faixas(ano_calendario, [f.dict() for f in parametros.faixas])

    saved_record = fetch_parametros(ano_calendario)
    if not saved_record:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível recuperar os parâmetros após a atualização.",
        )

    return IrParametros(**saved_record)


@router.post("/{ano_calendario}/faixas", response_model=List[IrFaixa])
def upsert_faixas_do_ano(ano_calendario: int, faixas: List[IrFaixa]) -> List[IrFaixa]:
    return [IrFaixa(**f) for f in upsert_faixas(ano_calendario, [f.dict() for f in faixas])]
