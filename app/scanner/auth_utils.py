import base64, json, hmac, hashlib, time
from django.conf import settings

SECRET = settings.SECRET_KEY.encode()

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + 7200,  
    }

    payload_json = json.dumps(payload).encode()
    b64 = base64.urlsafe_b64encode(payload_json)

    signature = hmac.new(SECRET, b64, hashlib.sha256).hexdigest()

    return f"{b64.decode()}.{signature}"


def verify_token(token):
    try:
        b64, signature = token.split(".")
        expected_sig = hmac.new(SECRET, b64.encode(), hashlib.sha256).hexdigest()

        if signature != expected_sig:
            return None

        payload = json.loads(base64.urlsafe_b64decode(b64.encode()))
        if payload["exp"] < time.time():
            return None

        return payload["user_id"]

    except:
        return None
