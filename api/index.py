import sys
import os

# ---------------------------------------------------------------------------
# Make the Flask app importable from app/app.py
# ---------------------------------------------------------------------------
# Vercel runs this file from the project root, so we add the `app/` directory
# to sys.path so that `from app import app` resolves to app/app.py correctly.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

# ---------------------------------------------------------------------------
# Import and re-export the Flask WSGI app object
# ---------------------------------------------------------------------------
# Vercel's Python runtime expects a WSGI callable named `app` in this file.
from app import app  # noqa: F401  (re-exported for Vercel)
