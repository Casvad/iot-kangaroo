from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from utils.rsa.key import PrivateKey


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    encrypted_pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public = pem_public_key.decode()
    private = encrypted_pem_private_key.decode()
    private_jwk = PrivateKey.load_pkcs1(private.encode('utf-8'))

    return {
        "public": public,
        "private": private,
        "jwk": {
            "coef": private_jwk.coef,
            "d": private_jwk.d,
            "e": private_jwk.e,
            "exp1": private_jwk.exp1,
            "exp2": private_jwk.exp2,
            "n": private_jwk.n,
            "p": private_jwk.p,
            "q": private_jwk.q,
        },
    }
