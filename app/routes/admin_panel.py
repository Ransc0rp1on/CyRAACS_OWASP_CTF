from flask import Blueprint, request, render_template
from app.db import get_db_connection

admin_panel = Blueprint("admin_panel", __name__)

@admin_panel.route("/sql-panel", methods=["GET", "POST"])
def sql_panel():
    leak  = None
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Enforce the special user 'elliot'
        if username.lower() != "elliot":
            error = "❌ Unknown user; login as ‘elliot’ to proceed."
            return render_template("sql_panel.html", leak=None, error=error)

        # Vulnerable query
        conn = get_db_connection()
        cur  = conn.cursor()
        query = f"""
            SELECT rc4_token
              FROM users
             WHERE username = '{username}'
               AND password = '{password}'
        """
        try:
            cur.execute(query)
            row = cur.fetchone()
            if row:
                leak = row[0]
        except Exception:
            pass
        finally:
            cur.close()
            conn.close()

    return render_template("sql_panel.html", leak=leak, error=error)
