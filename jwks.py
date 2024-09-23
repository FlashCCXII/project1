from flask import jsonify
from key_manager import keys
import time

def jwks():
    active_keys = [
        {"kid": key["kid"], "kty": "RSA", "alg": "RS256", "use": "sig", "n": key["public_key"].decode('utf-8')}
        for key in keys if key["expiry"] > time.time()
    ]
    return jsonify({"keys": active_keys})
