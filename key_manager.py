import uuid
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

keys = []

#Serialize private & public keys
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

#Create key w/ kid(key id) and expiration
def create_key():
    kid = str(uuid.uuid4())
    expiry = int(time.time()) + 3600  # 1 hour expiry
    private_key, public_key = generate_key_pair()

    return {
        "kid": kid,
        "expiry": expiry,
        "private_key": private_key,
        "public_key": public_key
    }


#Clean expired keys and manage new ones
def manage_keys():
    global keys
    new_key = create_key()
    keys.append(new_key)
    keys = [key for key in keys if key["expiry"] > time.time()]


#Regularly update keys
import threading


def start_key_manager():
    def run():
        while True:
            manage_keys()
            time.sleep(300)  #Every 5 mins

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
