import os
from flask import Flask

def create_app():
    """Application factory: creates Flask app and registers blueprints."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Use the SECRET_KEY from environment (fallback for dev)
    app.secret_key = os.getenv("SECRET_KEY", "default_dev_secret")

    # --- Register all blueprints ---
    try:
        # Import blueprints explicitly (package-style imports)
        from app.routes.entry import entry
        from app.routes.access import access
        from app.routes.auth import auth
        from app.routes.admin_panel import admin_panel
        from app.routes.crypto import crypto
        from app.routes.ssrf import ssrf
        from app.routes.logs import logs
        from app.routes.misconfig import misconfig

        # Register in one go
        for bp in (entry, access, auth, admin_panel, crypto, ssrf, logs, misconfig):
            app.register_blueprint(bp)

    except ImportError as e:
        raise RuntimeError(f"❌ Failed to import a blueprint: {e}")

    # --- Optional healthcheck route ---
    @app.route("/db-status")
    def db_status():
        try:
            from app.db import get_db_connection
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            cur.close()
            conn.close()
            return f"✅ Connected to PostgreSQL: {version}"
        except Exception as e:
            return f"❌ DB connection failed: {e}"

    return app
