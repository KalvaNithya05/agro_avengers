"""Run a simple SELECT against a Supabase table (default: profiles).

Usage:
  python scripts/test_db_query.py [table_name]

The script loads environment variables, initializes the Supabase client from
`backend.config.supabase_client`, and attempts a lightweight select.
"""
import os
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()

# Ensure project root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

table = sys.argv[1] if len(sys.argv) > 1 else "profiles"

try:
    from backend.config import supabase_client as sc
except Exception:
    print("Failed to import backend.config.supabase_client")
    traceback.print_exc()
    sys.exit(2)

client = sc.get_supabase_client()
print("Client type:", type(client))

def try_query():
    try:
        # Preferred: Postgrest API
        if hasattr(client, "postgrest"):
            post = client.postgrest
            if hasattr(post, "from_"):
                print(f"Querying table '{table}' via postgrest.from_().select().limit(5)")
                res = post.from_(table).select("*").limit(5).execute()
                print("Result:", getattr(res, 'data', res))
                return

        # Fallback: client.table(...) (older/alternate APIs)
        if hasattr(client, "table"):
            print(f"Querying table '{table}' via client.table().select().limit(5)")
            res = client.table(table).select("*").limit(5).execute()
            print("Result:", getattr(res, 'data', res))
            return

        print("No known query API available on client; using dummy or unsupported client.")
    except Exception:
        print("Query failed:")
        traceback.print_exc()

if __name__ == '__main__':
    try_query()
