import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Создает JWT-токен на основе предоставленных данных.

    Parameters:
        data (dict): Словарь данных, которые будут закодированы в токене.

    Returns:
        str: Сгенерированный JWT-токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Раскодирует JWT-токен и возвращает его содержимое (payload).

    Parameters:
        token (str): JWT-токен для раскодирования.

    Returns:
        dict: Содержимое токена (payload) в виде словаря.

    Raises:
        HTTPException: Если токен истек или недействителен, возбуждается исключение.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
