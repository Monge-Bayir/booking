from passlib.context import CryptContext

pwd_content = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_content.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)