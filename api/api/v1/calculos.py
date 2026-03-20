from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse

from ...repositories.calculo_repository import fetch_calculo_by_id, insert_calculo
from ...repositories.parametros_repository import fetch_parametros
from ...schemas.calculo import CalculoCreate, CalculoInput, CalculoInDB, CalculoResultado, TipoCalculo
from ...services.calculo_service import calcular_ajuste_anual, calcular_retificacao
from ...utils.pdf import render_relatorio_pdf

router = APIRouter(prefix="/calculos", tags=["calculos"])


@router.post("/simular", response_model=CalculoResultado)
def simular_calculo(entrada: CalculoInput) -> CalculoResultado:
    parametros_dict = fetch_parametros(entrada.ano_calendario)
    if not parametros_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parâmetros de IR não encontrados para o ano informado.",
        )

    from ...schemas.parametros import IrParametros

    parametros = IrParametros(**parametros_dict)

    try:
        if entrada.tipo_calculo == TipoCalculo.AJUSTE_ANUAL:
            return calcular_ajuste_anual(entrada, parametros)
        return calcular_retificacao(entrada, parametros)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao calcular: {str(e)}",
        )


@router.post("", response_model=CalculoInDB, status_code=status.HTTP_201_CREATED)
def criar_calculo(entrada: CalculoInput) -> CalculoInDB:
    try:
        resultado = simular_calculo(entrada)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao simular cálculo: {str(e)}",
        )

    payload = {
        "processo": entrada.processo,
        "tipo_calculo": entrada.tipo_calculo.value,
        "ano_calendario": entrada.ano_calendario,
        "dados_entrada": entrada.dict(),
        "resultado": resultado.dict(),
        "criado_em": datetime.utcnow().isoformat(),
    }

    record = insert_calculo(payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao persistir cálculo.",
        )

    return CalculoInDB(**record)


@router.get("/{calculo_id}", response_model=CalculoInDB)
def obter_calculo(calculo_id: str) -> CalculoInDB:
    record = fetch_calculo_by_id(calculo_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cálculo não encontrado")
    return CalculoInDB(**record)


@router.get("/{calculo_id}/pdf")
def gerar_pdf_calculo(
    calculo_id: str,
    response: Response,
    incluir_parametros: bool = Query(True, description="Inclui parâmetros de IR no PDF"),
) -> StreamingResponse:
    record = fetch_calculo_by_id(calculo_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cálculo não encontrado")

    parametros_dict = fetch_parametros(record["ano_calendario"])
    if not parametros_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parâmetros de IR não encontrados para o ano do cálculo.",
        )

    from ...schemas.parametros import IrParametros

    parametros = IrParametros(**parametros_dict)

    pdf_bytes = render_relatorio_pdf({
        "calculo": record,
        "parametros": parametros.dict(),
        "incluir_parametros": incluir_parametros,
    })

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=relatorio_{calculo_id}.pdf"
    return StreamingResponse(iter([pdf_bytes]), media_type="application/pdf")