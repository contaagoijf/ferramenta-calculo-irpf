from __future__ import annotations

from io import BytesIO
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

# WeasyPrint temporarily disabled on Windows (requires GTK libraries)
# Install GTK or use: pip install weasyprint

def render_relatorio_pdf(context: Dict[str, Any]) -> bytes:
    """PDF generation temporarily unavailable (WeasyPrint requires GTK on Windows)."""
    raise NotImplementedError(
        "PDF generation is disabled. Install GTK for Windows or use an alternative PDF library."
    )
