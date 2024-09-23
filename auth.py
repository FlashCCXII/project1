from flask import request, jsonify
from key_manager import keys
import time
import jwt


def auth():
    use_expired = request.args.get('expired', 'false').lower() == 'true'

    if use_expired:
        expired_key = [key for key in keys if key["expiry"] <= time.time()]
        key_to_use = expired_key[0] if expired_key else None
    else:
        active_key = [key for key in keys if key["expiry"] > time.time()]
        key_to_use = active_key[0] if active_key else None

    if key_to_use:
        token = jwt.encode(
            {"sub": "1234567890", "name": "John Doe", "admin": True, "exp": key_to_use["expiry"]},
            key_to_use["private_key"],
            algorithm="RS256",
            headers={"kid": key_to_use["kid"]}
        )
        return jsonify({"token": token})
    else:
        return jsonify({"error": "No valid key found"}), 400
