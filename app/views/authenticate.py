from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..database import get_db
from ..schemas import UserSignUp, UserSignUpResponse
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash_password
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