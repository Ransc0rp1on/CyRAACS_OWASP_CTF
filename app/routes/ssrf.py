from flask import Blueprint, request, redirect, render_template
import requests

ssrf = Blueprint("ssrf", __name__)

@ssrf.route("/ssrf")
def ssrf_route():
    url = request.args.get("url")
    if not url:
        return render_template("ssrf.html", error="Missing URL parameter")

    try:
        # Simulate internal-only access
        if "127.0.0.1" not in url and "localhost" not in url:
            return render_template("ssrf.html", error="Access denied: only internal IPs allowed")

        response = requests.get(url, timeout=2)
        if "/internal" in url:
            return redirect("/v1/internal/log_view")
        return f"Fetched internal response: {response.text}"
    except Exception as e:
        return render_template("ssrf.html", error=str(e))
