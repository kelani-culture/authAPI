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

def create_access_token(data: dict, expire_min: timedelta | None = None):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_MIN)
    data_copy.update({"exp": expire})
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str, credential_exception):
    try:
        print('all gooooood')
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = token_decode.get('id')
        username = token_decode.get('username')
        is_verified = token_decode.get('is_verified')
        print(token_decode)
        if id is None or is_verified is None or username is None:
            raise credential_exception
        data = TokenData(id=id, is_verified=is_verified, username=username)
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