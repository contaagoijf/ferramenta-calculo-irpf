from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, PositiveInt, condecimal


Currency = condecimal(max_digits=18, decimal_places=2)
Aliquota = condecimal(max_digits=10, decimal_places=4)


class IrFaixa(BaseModel):
    id: int
    ano_calendario: PositiveInt
    limite_inferior: Currency
    limite_superior: Optional[Currency]  # NULL para a última faixa
    aliquota: Aliquota
    deducao: Currency


class IrParametros(BaseModel):
    ano_calendario: PositiveInt
    teto: Currency
    inicio_correcao: date
    faixas: List[IrFaixa]
