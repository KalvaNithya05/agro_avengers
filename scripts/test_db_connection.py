"""Simple DB connection test for Supabase.

Usage:
  pip install -r requirements.txt
  python scripts/test_db_connection.py

This script checks for `SUPABASE_URL` and `SUPABASE_KEY` in the environment,
initializes the client using `backend.config.supabase_client`, and attempts a
simple HTTP GET to the Supabase URL to verify reachability.
"""
import os
import sys
import traceback
from dotenv import load_dotenv
import requests

# Make sure project root is on sys.path so `backend` package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure project's root .env is loaded
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def masked(val: str) -> str:
    if not val:
        return "<missing>"
    if len(val) <= 8:
        return "<present>"
    return val[:4] + "..." + val[-4:]

def main():
    print("SUPABASE_URL:", masked(SUPABASE_URL))
    print("SUPABASE_KEY:", masked(SUPABASE_KEY))

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set. Aborting.")
        sys.exit(2)

    # Try to initialize client from project's module
    try:
        from backend.config import supabase_client as sc
    except Exception as e:
        print("Failed to import backend.config.supabase_client:")
        traceback.print_exc()
        sys.exit(3)

    client = None
    try:
        client = sc.get_supabase_client()
        print("get_supabase_client() returned:", type(client))
    except Exception:
        print("Exception while calling get_supabase_client():")
        traceback.print_exc()

    # Basic network reachability check
    try:
        print(f"Attempting HTTP GET to {SUPABASE_URL} (timeout=6s)")
        resp = requests.get(SUPABASE_URL, timeout=6)
        print("HTTP status:", resp.status_code)
    except Exception as e:
        print("HTTP request failed:")
        traceback.print_exc()

    # If client was created, try a lightweight PostgREST call if available
    if client is not None:
        try:
            # Attempt to list schemas via the PostgREST root (may require auth)
            print("Attempting lightweight PostgREST GET via client.postgrest")
            r = client.postgrest.get("/")
            print("postgrest GET result type:", type(r))
        except Exception:
            print("postgrest request failed:")
            traceback.print_exc()

    print("Done.")

if __name__ == '__main__':
    main()
