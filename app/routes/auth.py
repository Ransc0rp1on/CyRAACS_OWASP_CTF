# app/routes/auth.py
from flask import Blueprint, request, session, redirect, flash

auth = Blueprint("auth", __name__)

@auth.route("/jwt-reset")
def jwt_reset():
    # Validate challenge progression
    if session.get("access_stage") != 2:
        flash("❌ Complete the profile challenge first", "danger")
        return redirect("/")
    
    # Validate token
    token = request.args.get("token", "")
    if token == "bypass_alg_none":
        session["access_stage"] = 3  # Grant access to SQL panel
        return redirect("/sql-panel")
    else:
        flash("❌ Invalid JWT bypass token", "danger")
        return redirect("/creddle-note")