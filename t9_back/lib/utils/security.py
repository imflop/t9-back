import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
