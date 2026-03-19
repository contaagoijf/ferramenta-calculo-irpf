from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from ..core.supabase import get_supabase_client


def insert_calculo(calculo: Dict[str, Any]) -> Dict[str, Any]:
    """Insere um cálculo na tabela `calculos`."""
    client = get_supabase_client()
    result = (
        client.table("calculos")
        .insert(calculo)
        .select("*")
        .single()
        .execute()
    )
    return result.data


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