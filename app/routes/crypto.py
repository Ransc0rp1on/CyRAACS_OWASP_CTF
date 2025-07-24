from flask import Blueprint, request, render_template, make_response
import zlib
from Crypto.Cipher import ARC4

crypto = Blueprint("crypto", __name__)

RC4_KEY = b'MY_FIXED_RC4_KEY'
SECRET  = b"/ssrf?url=http://internal:5000/internal"

@crypto.route('/sql-panel/crack', methods=["GET"])
def crack():
    guess = request.args.get('data', '')
    try:
        payload = (guess + SECRET.decode()).encode()
    except Exception:
        return render_template('crack.html', response_length=None, error="Invalid input")

    compressed = zlib.compress(payload)
    ciphertext = ARC4.new(RC4_KEY).encrypt(compressed)

    resp = make_response(ciphertext)
    resp.headers['Content-Type'] = 'application/octet-stream'
    resp.headers['Content-Length'] = str(len(ciphertext))
    return resp
