from hashlib import sha512

from config import KEY

def password_hash(password: str) -> str:
    sha = sha512(KEY.encode())
    sha.update(password.encode())
    return sha.hexdigest()
