from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from ..schemas.calculo import CalculoInput, CalculoResultado, TipoDeclaracao
from ..schemas.parametros import IrFaixa, IrParametros


def _normalize_decimal(value: Decimal) -> Decimal:
    # Ensure consistent quantization to two decimal places for determinism.
    return value.quantize(Decimal("0.01"))


def _apply_limits(value: Decimal, minimo: Decimal = Decimal("0")) -> Decimal:
    return max(minimo, _normalize_decimal(value))


def _find_faixa(base_calculo: Decimal, faixas: List[IrFaixa]) -> Optional[IrFaixa]:
    # A tabela de faixas usa `limite_superior` como exclusivo.
    # A última faixa tem `limite_superior = None` (sem limite máximo).
    for faixa in sorted(faixas, key=lambda f: f.limite_inferior):
        if faixa.limite_superior is None:
            # Última faixa: aplica se base_calculo >= limite_inferior
            if base_calculo >= faixa.limite_inferior:
                return faixa
        else:
            # Faixas intermediárias: aplica se limite_inferior <= base_calculo < limite_superior
            if faixa.limite_inferior <= base_calculo < faixa.limite_superior:
                return faixa

    return None


def calcular_ajuste_anual(
    entrada: CalculoInput, parametros: IrParametros
) -> CalculoResultado:
    """Calcula o ajuste anual de IRPF seguindo as fórmulas do PRD.

    Etapas principais:
      1. Calcular base de cálculo inicial conforme tipo de declaração.
      2. Determinar alíquota e dedução a partir das faixas de IR.
      3. Calcular imposto devido (incluindo incentivos e imposto RRA).
      4. Recalcular valores considerando ajustes fornecidos pelo usuário.
      5. Definir saldo a pagar / restituir.

    Todos os cálculos são determinísticos e normalizados para 2 casas decimais.
    """

    teto = _normalize_decimal(parametros.teto)

    # --- Cálculo inicial (antes de ajustes) ---
    rend_tribut = _normalize_decimal(entrada.rendimentos_tributaveis)

    if entrada.tipo_declaracao == TipoDeclaracao.SIMPLIFICADA:
        total_deducoes = min(_normalize_decimal(rend_tribut * Decimal("0.2")), teto)
    else:
        total_deducoes = _normalize_decimal(entrada.deducoes_legais)

    base_calculo = _apply_limits(rend_tribut - total_deducoes)

    faixa = _find_faixa(base_calculo, parametros.faixas)
    if faixa is None:
        raise ValueError("Não foi possível determinar a faixa de IR para o ano informado")

    aliquota_inicial = faixa.aliquota
    deducao_inicial = faixa.deducao

    imposto_devido = _apply_limits(
        (base_calculo * aliquota_inicial)
        - deducao_inicial
        - _normalize_decimal(entrada.deducoes_incentivo)
        + _normalize_decimal(entrada.imposto_rra)
    )

    # --- Recalculo (com ajustes fornecidos pelo usuário) ---
    rend_tribut_recalc = _normalize_decimal(
        rend_tribut + entrada.rend_somar - entrada.rend_sub
    )

    if entrada.tipo_declaracao == TipoDeclaracao.SIMPLIFICADA:
        total_deducoes_recalc = min(
            _normalize_decimal(rend_tribut_recalc * Decimal("0.2")), teto
        )
        incentivo_recalc = Decimal("0")
    else:
        total_deducoes_recalc = _normalize_decimal(
            entrada.deducoes_legais + entrada.ded_somar - entrada.ded_sub
        )
        incentivo_recalc = _normalize_decimal(
            entrada.deducoes_incentivo + entrada.incentivo_somar - entrada.incentivo_sub
        )

    base_calculo_recalc = _apply_limits(rend_tribut_recalc - total_deducoes_recalc)

    imposto_rra_recalc = _normalize_decimal(
        entrada.imposto_rra + entrada.rra_somar - entrada.rra_sub
    )

    faixa_recalc = _find_faixa(base_calculo_recalc, parametros.faixas)
    if faixa_recalc is None:
        raise ValueError("Não foi possível determinar a faixa de IR para o ano informado")

    aliquota_recalc = faixa_recalc.aliquota
    deducao_recalc = faixa_recalc.deducao

    imposto_devido_recalc = _apply_limits(
        (base_calculo_recalc * aliquota_recalc)
        - deducao_recalc
        - incentivo_recalc
        + imposto_rra_recalc
    )

    imposto_pago = _apply_limits(entrada.imposto_pago)
    imposto_a_pagar = _normalize_decimal(imposto_devido_recalc - imposto_pago)

    tipo_saldo = "a_pagar" if imposto_a_pagar > 0 else "restituicao"

    resultado: CalculoResultado = CalculoResultado(
        base_calculo=base_calculo_recalc,
        imposto_devido=imposto_devido_recalc,
        imposto_pago=imposto_pago,
        saldo=imposto_a_pagar,
        tipo_saldo=tipo_saldo,
        detalhes={
            "teto": teto,
            "total_deducoes": total_deducoes,
            "base_calculo": base_calculo,
            "aliquota_inicial": aliquota_inicial,
            "deducao_inicial": deducao_inicial,
            "imposto_devido": imposto_devido,
            "rend_tribut_recalc": rend_tribut_recalc,
            "total_deducoes_recalc": total_deducoes_recalc,
            "base_calculo_recalc": base_calculo_recalc,
            "imposto_rra_recalc": imposto_rra_recalc,
            "incentivo_recalc": incentivo_recalc,
            "aliquota_recalc": aliquota_recalc,
            "deducao_recalc": deducao_recalc,
            "imposto_devido_recalc": imposto_devido_recalc,
            "imposto_a_pagar": imposto_a_pagar,
        },
    )

    return resultado


def calcular_retificacao(entrada: CalculoInput, parametros: IrParametros) -> CalculoResultado:
    """Estrutura inicial para cálculo de retificação.

    As regras específicas ainda não foram definidas no MVP, então a implementação
    atual reutiliza o cálculo de ajuste anual como placeholder.
    """
    return calcular_ajuste_anual(entrada, parametros)