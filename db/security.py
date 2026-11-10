from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хэширует пароль для хранения в БД."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Проверяет, что введённый пароль соответствует хэшу из БД."""
    return _pwd_context.verify(plain_password, password_hash)