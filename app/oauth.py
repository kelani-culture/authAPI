from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings
from .schemas import TokenData
from fastapi import Depends, HTTPException, status

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

ALGORITHM=settings.algorithm
SECRET_KEY=settings.secret_key
ACCESS_TOKEN_MIN=settings.access_token_min

def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MIN)
    data_copy.update({"exp": expire})
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str, credential_exception):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = token_decode.get('user_id')
        is_super = token_decode.get('is_super')
        is_admin = token_decode.get('is_admin')
        if id is None or is_super is None or is_admin is None:
            raise credential_exception
        data = TokenData(id=id, is_super=is_super, is_admin=is_admin)
    except JWTError:
        raise credential_exception
    return data

    
    
def get_current_user(token: str=Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)