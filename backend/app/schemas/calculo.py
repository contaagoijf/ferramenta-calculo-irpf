from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, PositiveInt, condecimal, constr, validator


class TipoCalculo(str, Enum):
    AJUSTE_ANUAL = "ajuste_anual"
    RETIFICACAO = "retificacao"


class TipoDeclaracao(str, Enum):
    COMPLETA = "completa"
    SIMPLIFICADA = "simplificada"


Currency = condecimal(max_digits=18, decimal_places=2)


class CalculoInput(BaseModel):
    processo: constr(strip_whitespace=True, min_length=1)
    nome_autor: constr(strip_whitespace=True, min_length=1)
    tipo_declaracao: TipoDeclaracao
    ano_calendario: PositiveInt

    rendimentos_tributaveis: Currency = Field(..., ge=0)
    deducoes_legais: Currency = Field(0, ge=0)
    deducoes_incentivo: Currency = Field(0, ge=0)
    imposto_rra: Currency = Field(0, ge=0)
    imposto_pago: Currency = Field(0, ge=0)

    rend_somar: Currency = Field(0, ge=0)
    rend_sub: Currency = Field(0, ge=0)
    ded_somar: Currency = Field(0, ge=0)
    ded_sub: Currency = Field(0, ge=0)
    incentivo_somar: Currency = Field(0, ge=0)
    incentivo_sub: Currency = Field(0, ge=0)
    rra_somar: Currency = Field(0, ge=0)
    rra_sub: Currency = Field(0, ge=0)

    tipo_calculo: TipoCalculo = TipoCalculo.AJUSTE_ANUAL

    @validator("deducoes_legais", always=True)
    def validate_deducoes_legais(cls, v, values):
        if values.get("tipo_declaracao") == TipoDeclaracao.SIMPLIFICADA and v != 0:
            raise ValueError("Deduções legais só podem ser informadas na declaração completa")
        return v

    @validator("deducoes_incentivo", always=True)
    def validate_deducoes_incentivo(cls, v, values):
        if values.get("tipo_declaracao") == TipoDeclaracao.SIMPLIFICADA and v != 0:
            raise ValueError("Deduções de incentivo só podem ser informadas na declaração completa")
        return v


class CalculoResultado(BaseModel):
    base_calculo: Currency
    imposto_devido: Currency
    imposto_pago: Currency
    saldo: Currency
    tipo_saldo: str
    detalhes: Dict[str, Any]


class CalculoCreate(BaseModel):
    dados_entrada: CalculoInput
    resultado: CalculoResultado


class CalculoInDB(BaseModel):
    id: str
    processo: str
    tipo_calculo: TipoCalculo
    ano_calendario: PositiveInt
    dados_entrada: Dict[str, Any]
    resultado: Optional[Dict[str, Any]]
    criado_em: datetime

    class Config:
        orm_mode = True


class CalculoResponse(BaseModel):
    id: str
    processo: str
    tipo_calculo: TipoCalculo
    ano_calendario: PositiveInt
    dados_entrada: Dict[str, Any]
    resultado: Optional[Dict[str, Any]]
    criado_em: datetime
