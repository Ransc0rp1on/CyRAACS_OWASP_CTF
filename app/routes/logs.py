from flask import Blueprint, render_template

logs = Blueprint("logs", __name__)

@logs.route("/v1/internal/log_view")
def view_logs():
    # Final flag (could be generated or pulled from DB for more realism)
    final_flag = "flag{CR1M3_CR4CK}"
    return render_template("log_view.html", flag=final_flag)
