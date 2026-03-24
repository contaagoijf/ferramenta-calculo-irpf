from __future__ import annotations

from typing import Any, Dict, List, Optional

from postgrest.exceptions import APIError

from app.core.supabase import get_supabase_client


def _extract_single_row(data: Any) -> Optional[Dict[str, Any]]:
    if isinstance(data, list):
        return data[0] if data else None
    return data


def fetch_parametros(ano_calendario: int) -> Optional[Dict[str, Any]]:
    """Retorna os parametros de IR juntamente com as faixas."""
    client = get_supabase_client()

    try:
        parametros_res = (
            client.table("ir_parametros")
            .select("*")
            .eq("ano_calendario", ano_calendario)
            .single()
            .execute()
        )
    except APIError as exc:
        if getattr(exc, "code", None) == "PGRST116":
            return None
        raise

    parametros = parametros_res.data
    if not parametros:
        return None

    faixas_res = (
        client.table("ir_faixas")
        .select("*")
        .eq("ano_calendario", ano_calendario)
        .order("limite_inferior", desc=False)
        .execute()
    )

    parametros["faixas"] = faixas_res.data or []
    return parametros


def upsert_parametros(parametros: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Cria ou atualiza parametros para um ano calendario."""
    client = get_supabase_client()
    result = client.table("ir_parametros").upsert(parametros, on_conflict="ano_calendario").execute()
    return _extract_single_row(result.data)


def upsert_faixas(ano_calendario: int, faixas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    client = get_supabase_client()
    payload = [{**faixa, "ano_calendario": ano_calendario} for faixa in faixas]

    result = client.table("ir_faixas").upsert(payload, on_conflict="id").execute()
    return result.data or []
