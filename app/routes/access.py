# app/routes/access.py
from flask import Blueprint, render_template, redirect, session, flash, url_for

access = Blueprint("access", __name__)

@access.route("/creddle-note")
def creddle_note():
    if session.get("access_stage") != 1:
        flash("❌ Complete the file upload challenge first", "danger")
        return redirect(url_for("entry.upload"))
    return render_template("creddle_note.html")

@access.route("/profile/<int:user_id>")
def profile(user_id):
    if session.get("access_stage") != 1:
        flash("❌ Access to profiles requires completing previous challenges", "danger")
        return redirect(url_for("entry.upload"))
    
    if user_id == 7:
        # Set to stage 2 for JWT challenge (not 3)
        session["access_stage"] = 2
        token = "bypass_alg_none"
        return render_template("profile_success.html", token=token)
    
    flash(f"⚠️ Access denied for profile #{user_id}", "warning")
    return render_template("profile_denied.html"), 403