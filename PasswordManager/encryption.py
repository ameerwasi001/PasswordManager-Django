import binascii
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

backend = default_backend()
iterations = 100_000

def derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def get_new_key() -> bytes:
    return Fernet.generate_key()


def whole_encrypt(data: str, password: str):
    key = get_new_key()
    enc_data = encrypt(data.encode(), key)
    enc_key = password_encrypt(key, password)
    return (enc_key.decode(), enc_data.decode())

def whole_decrypt(enc_data: str, enc_key: str, password: str):
    key = password_decrypt(enc_key.encode(), password)
    return decrypt(enc_data.encode(), key).decode()

def generate_rsa_keys(password: str):
    key = rsa.generate_private_key(
        backend=backend,
        public_exponent=65537,
        key_size=3072
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(password.encode())
    ).decode("utf-8")
    public_key = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    return (public_key, private_key) 

def rsa_encrypt(public_key_str: str, message: str):
    public_key = serialization.load_pem_public_key(public_key_str.encode())
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return binascii.b2a_hex(ciphertext).decode()

def rsa_decrypt(private_key_str: str, password: str, ciphertext: str):
    private_key = serialization.load_pem_private_key(
        private_key_str.encode(),
        password=password.encode(),
    )
    plaintext = private_key.decrypt(
        binascii.a2b_hex(ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

# encrypted = rsa_encrypt(pub_key, "Hi There, hello")
# orig = rsa_decrypt(priv_key, "mx12345678", encrypted)
# print(orig)

# print(
#     password_decrypt(
#         "uHZH1sm2tJAw_dDpqVSGiQABhqCAAAAAAGHMPP049qYh8K6_up6QDAPZu-k8FrioraG0qWf8xptM0mspa6Une6JuRMZjwNNZZNGnYocRADETVTTNfr46zuShkWWfW5fNT2cJ1gSow1QycdcgXfWRHzYC9rJsSWP_Grg6VvI=".encode(),
#         "mx12345678"
#     )
# )

# enc_key, enc_data = whole_encrypt("Hello there", "mx12345678")
# print(whole_decrypt(enc_data, enc_key, "mx12345678"))