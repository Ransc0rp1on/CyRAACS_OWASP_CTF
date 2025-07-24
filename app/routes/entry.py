# Entry blueprint (upload challenge)
from flask import Blueprint, render_template, request, redirect, session, flash, url_for

entry = Blueprint("entry", __name__)

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

@entry.route("/", methods=["GET", "POST"])
def upload():
    # Reset session when returning to upload page
    session.pop("access_stage", None)
    
    if request.method == "POST":
        if "file" not in request.files:
            flash("❌ No file uploaded", "danger")
            return redirect(url_for("entry.upload"))
            
        file = request.files["file"]
        
        if file.filename == '':
            flash("❌ No file selected", "danger")
            return redirect(url_for("entry.upload"))
            
        if not ('.' in file.filename and file.filename.lower().endswith('.png')):
            flash("❌ Invalid file type. Only PNG files allowed.", "danger")
            return redirect(url_for("entry.upload"))

        contents = file.read()
        
        if len(contents) < 8 or contents[:8] != PNG_SIGNATURE:
            flash("❌ Invalid PNG signature. File must start with proper PNG header bytes.", "danger")
            return redirect(url_for("entry.upload"))
        
        if b'\x50\x4B\x03\x04' in contents:
            session["access_stage"] = 1  # Successful upload
            return redirect(url_for("access.creddle_note"))
        else:
            flash("✅ Valid PNG detected but no payload found. File must contain special markers.", "warning")
            return redirect(url_for("entry.upload"))

    return render_template("upload.html")