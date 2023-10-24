from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..schemas import (UserSignUp, UserSignUpResponse,
                       SignIn, SignInResponse)
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash_password, verify_pwd
from ..oauth import create_access_token
"""
This files covers both user signup, login and
logout authentication
"""
router = APIRouter(
    tags=['authentication']
)


@router.get('/')
def root():
    return {'message': 'welcome to my api'}



@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=UserSignUpResponse)
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    """
        Register user to the app user signup authenitcation
    """
    get_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    get_phone = db.query(models.Users).filter(models.Users.phone_number == user.phone_number).\
                first()
    if get_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                             detail='email already used')
    if get_phone:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
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
def login(user: SignIn, db: Session=Depends(get_db)):
    user_cred = db.query(models.Users).filter(models.Users.email==user.email).first()
    if not user_cred:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='email does not exist')
    hashed_pwd = verify_pwd(user.password, user_cred.password) 
    if not hashed_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect password') 

    access_token = create_access_token({'user_id': user_cred.id})
    return {'token': access_token, 'token_type': "Bearer"}