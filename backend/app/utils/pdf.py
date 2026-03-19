from __future__ import annotations

from io import BytesIO
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML


def render_relatorio_pdf(context: Dict[str, Any]) -> bytes:
    """Renderiza um relatório em PDF a partir de um template HTML."""

    env = Environment(
        loader=FileSystemLoader("app/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("relatorio.html")
    html_content = template.render(**context)

    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return pdf_io.read()
