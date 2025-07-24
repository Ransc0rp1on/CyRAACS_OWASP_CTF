from flask import Blueprint, render_template

misconfig = Blueprint("misconfig", __name__)

@misconfig.route("/logz")
@misconfig.route("/admin-log")
@misconfig.route("/logs")
@misconfig.route("/hidden-log")
def fake_logs():
    return render_template("404.html"), 404
