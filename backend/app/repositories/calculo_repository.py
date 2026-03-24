from __future__ import annotations

from typing import Any, Dict, Optional

from app.core.supabase import get_supabase_client


def _extract_single_row(data: Any) -> Optional[Dict[str, Any]]:
    if isinstance(data, list):
        return data[0] if data else None
    return data


def insert_calculo(calculo: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Insere um calculo na tabela `calculos`."""
    client = get_supabase_client()
    result = client.table("calculos").insert(calculo).execute()
    return _extract_single_row(result.data)


def fetch_calculo_by_id(calculo_id: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    result = (
        client.table("calculos")
        .select("*")
        .eq("id", calculo_id)
        .single()
        .execute()
    )
    return result.data
