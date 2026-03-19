from supabase import create_client

from .config import settings


def get_supabase_client():
    """Returns a Supabase client instance configured via environment variables."""
    return create_client(settings.supabase_url, settings.supabase_key)