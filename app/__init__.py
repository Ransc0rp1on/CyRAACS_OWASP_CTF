# app/__init__.py
import os
from flask import Flask

def create_app():
    """Application factory: creates Flask app and registers blueprints."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    # Use the SECRET_KEY from env
    app.secret_key = os.getenv("SECRET_KEY", "default_dev_secret")

    # Register all of your route blueprints
    from .routes.entry        import entry
    from .routes.access       import access
    from .routes.auth         import auth
    from .routes.admin_panel  import admin_panel
    from .routes.crypto       import crypto
    from .routes.ssrf         import ssrf
    from .routes.logs         import logs
    from .routes.misconfig    import misconfig

    for bp in (entry, access, auth, admin_panel, crypto, ssrf, logs, misconfig):
        app.register_blueprint(bp)

    # Optional healthcheck
    @app.route("/db-status")
    def db_status():
        from .db import get_db_connection
        try:
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
