"""
Vercel entrypoint for the FastAPI application.

This file lives in the repository root `api/` directory because Vercel
detects Python functions there by default.
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

__all__ = ["app"]
