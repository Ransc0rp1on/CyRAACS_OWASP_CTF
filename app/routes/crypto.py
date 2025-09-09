from flask import Blueprint, request, make_response
import zlib
import random
import string
from Crypto.Cipher import ARC4

crypto = Blueprint("crypto", __name__)

# Configuration
SECRET = b"/ssrf?url=http://internal:5000/internal"  # Hidden challenge hint
# Random RC4 key generated once per server start
RC4_KEY = ''.join(random.sample(string.ascii_uppercase + string.digits, k=17)).encode()

def encrypt(msg: bytes) -> bytes:
    """Compress and encrypt data using RC4"""
    cipher = ARC4.new(RC4_KEY)
    compressed = zlib.compress(msg)
    return cipher.encrypt(compressed)

@crypto.route('/sql-panel/crack', methods=["GET"])
def crack():
    """Compression oracle endpoint"""
    user_input = request.args.get('data', '')

    # Construct response text including user input and hidden secret
    response_text = f"Input: {user_input} | Secret: {SECRET.decode()}"

    # Encrypt the response
    encrypted_response = encrypt(response_text.encode())

    # Return ciphertext with Content-Length leak
    resp = make_response(encrypted_response)
    resp.headers['Content-Type'] = 'application/octet-stream'
    resp.headers['Content-Length'] = str(len(encrypted_response))
    return resp
