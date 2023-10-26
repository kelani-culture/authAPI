from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..schemas import (UserSignUp, UserSignUpResponse,
                       SignIn, SignInResponse)
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash_password, verify_pwd
from ..oauth import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
"""
This files covers both user signup, login and
logout authentication
"""
router = APIRouter(
    tags=['authentication']
)




@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=UserSignUpResponse)
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    """
        Register user to the app user signup authenitcation
    """
    get_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    get_phone = db.query(models.Users).filter(models.Users.phone_number == user.phone_number).\
                first()
    get_username = db.query(models.Users).filter(models.Users.username == user.username).first()

    if get_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User name already exists')
    if get_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail='email already exists')
    if get_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail='phone number already used')
    user_dict = user.dict()
    hashed_pwd = hash_password(user_dict['password'])
    user_dict.pop('confirm_password')
    user_dict['password'] = hashed_pwd
    user_details = models.Users(**user_dict)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
    return user_details


@router.post('/login', status_code=status.HTTP_200_OK,
            response_model=SignInResponse)
def login(user:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user_cred = db.query(models.Users).filter(models.Users.email==user.username).first()
    if not user_cred:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='email does not exist')
    hashed_pwd = verify_pwd(user.password, user_cred.password) 
    if not hashed_pwd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect password')
    
    data = {
        'user_id': user_cred.id,
        'is_super': user_cred.is_superuser,
        'is_admin': user_cred.is_admin
    }
    access_token = create_access_token(data)
    return {'token': access_token, 'token_type': "Bearer"}