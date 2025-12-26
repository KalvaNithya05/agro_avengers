import os
from dotenv import load_dotenv

# Optional import; keep import-time failures isolated
try:
    from supabase import create_client, Client
except Exception:  # pragma: no cover - optional dependency
    create_client = None
    Client = object

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class _DummyPostgrest:
    def get(self, path: str):
        print(f"[supabase_client] Dummy postgrest.get called with: {path}")
        return []


class _DummyClient:
    def __init__(self):
        self.postgrest = _DummyPostgrest()


def get_supabase_client() -> Client:
    """Initializes and returns the Supabase client.

    If `SUPABASE_URL`/`SUPABASE_KEY` are missing, a lightweight dummy client is
    returned for local development/testing so code paths depending on
    `client.postgrest.get(...)` can still run.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables. Using dummy client for local development.")
        return _DummyClient()

    # Detect obvious placeholder values and treat them as missing
    lower_url = (SUPABASE_URL or "").lower()
    if "your-project-ref" in lower_url or "your-" in lower_url or "example" in lower_url:
        print("Warning: SUPABASE_URL looks like a placeholder. Using dummy client for local development.")
        return _DummyClient()

    if create_client is None:
        print("Warning: `supabase` package not available in this environment. Using dummy client.")
        return _DummyClient()

    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}\nUsing dummy client instead.")
        return _DummyClient()


# Create a global instance
supabase = get_supabase_client()
