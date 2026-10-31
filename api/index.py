import os
import sys
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel entrypoint callable
app = application

# Automatic migration & seed on startup if configured in Vercel environment
if os.environ.get("AUTO_MIGRATE", "").lower() in ("1", "true", "yes"):
    try:
        from django.core.management import call_command
        call_command("migrate", interactive=False)
        if os.environ.get("AUTO_SEED", "").lower() in ("1", "true", "yes"):
            call_command("seed_evaluation", interactive=False)
    except Exception as exc:
        print(f"[Vercel Startup] Migration/Seed warning: {exc}", file=sys.stderr)
