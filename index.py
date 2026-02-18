import os
import sys

# Force output flushing for Vercel logs
print("--- [VERCEL] STARTING INDEX.PY LOADING ---", flush=True)

# Add current directory to sys.path to find local modules like 'api', 'proto', 'byte'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("--- [VERCEL] ATTEMPTING TO IMPORT API ---", flush=True)
    from api import app
    print("--- [VERCEL] API IMPORT SUCCESSFUL ---", flush=True)
except Exception as e:
    print(f"--- [VERCEL] FATAL ERROR IMPORTING API: {e} ---", flush=True)
    import traceback
    traceback.print_exc()
    # We must raise the error so Vercel knows deployment failed, but at least we logged it first
    raise e
