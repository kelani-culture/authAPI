from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings

oauth_schemas = OAuth2PasswordBearer('login')

ALGORITHM=settings.algorithm
SECRET_KEY=settings.secret_key
ACCESS_TOKEN_MIN=settings.access_token_min

def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MIN)
    data_copy.update({"exp": expire})
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token
