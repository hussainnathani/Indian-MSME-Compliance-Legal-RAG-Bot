"""
Configuration module — loads environment variables and initializes clients.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    # First try os.environ
    val = os.getenv(key)
    if not val:
        # Try Streamlit secrets if running in Streamlit
        try:
            import streamlit as st
            val = st.secrets.get(key)
        except Exception:
            pass
    if val:
        # Strip accidental quotes and whitespace that happen when pasting into Streamlit Secrets
        return str(val).strip().strip('"').strip("'")
    return default

# ─── Supabase ───────────────────────────────────────────────
SUPABASE_URL = get_secret("SUPABASE_URL", "")
SUPABASE_KEY = get_secret("SUPABASE_KEY", "")

# ─── Google Gemini ──────────────────────────────────────────
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY", "")

# ─── RAG Settings ───────────────────────────────────────────
CHUNK_SIZE = 500          # characters per chunk
CHUNK_OVERLAP = 50        # overlap between chunks
MATCH_THRESHOLD = 0.5     # cosine similarity threshold
MATCH_COUNT = 5           # top-K results to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "gemini-2.5-flash"
