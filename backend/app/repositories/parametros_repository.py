from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.supabase import get_supabase_client


def fetch_parametros(ano_calendario: int) -> Optional[Dict[str, Any]]:
    """Retorna os parâmetros de IR (teto, início correção) juntamente com as faixas."""
    client = get_supabase_client()

    parametros_res = (
        client.table("ir_parametros")
        .select("*")
        .eq("ano_calendario", ano_calendario)
        .single()
        .execute()
    )
    parametros = parametros_res.data
    if not parametros:
        return None

    faixas_res = (
        client.table("ir_faixas")
        .select("*")
        .eq("ano_calendario", ano_calendario)
        .order("limite_inferior", ascending=True)
        .execute()
    )

    parametros["faixas"] = faixas_res.data or []
    return parametros


def upsert_parametros(parametros: Dict[str, Any]) -> Dict[str, Any]:
    """Cria ou atualiza parâmetros para um ano calendário.

    Observação: esta função faz "upsert" somente na tabela `ir_parametros`.
    As faixas devem ser atualizadas separadamente.
    """
    client = get_supabase_client()
    result = (
        client.table("ir_parametros")
        .upsert(parametros, on_conflict="ano_calendario")
        .select("*")
        .single()
        .execute()
    )
    return result.data


def upsert_faixas(ano_calendario: int, faixas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    client = get_supabase_client()
    # Supabase upsert requires unique keys; we assume `id` exists when updating.
    # We'll upsert by composing the payload.
    payload = []
    for faixa in faixas:
        payload.append({**faixa, "ano_calendario": ano_calendario})

    result = (
        client.table("ir_faixas")
        .upsert(payload, on_conflict="id")
        .select("*")
        .execute()
    )
    return result.data or []
