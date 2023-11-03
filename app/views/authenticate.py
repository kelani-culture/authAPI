from fastapi import APIRouter, Depends, HTTPException, Request, status
from ..database import get_db
from ..schemas import (UserSignUp, UserSignUpResponse,
                       SignIn, SignInResponse)
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash_password, verify_pwd
from ..oauth import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from ..oauth import verify_token
from mails import *
"""
This files covers both user signup, login and
logout authentication
"""
router = APIRouter(
    tags=['authentication']
)

#templates
from fastapi.templating import Jinja2Templates

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignUp, db: Session = Depends(get_db)):
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
    # not saving confirm password to db
    user_dict.pop('confirm_password')
    user_dict['password'] = hashed_pwd
    user_details = models.Users(**user_dict)
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
    email_details = {
        'id': user_details.id,
        'username': user_details.username,
        'is_verified': user_details.is_verified,
    }
    await send_email([user_dict['email']], email_details)
    return {
        "status": 201,
        "message": f"Hello {user_details.username} thanks for registring with us "+\
            f"please check your inbox for a verification mail"
    } 

templates = Jinja2Templates(directory="templates")
@router.get('/verification', response_class=HTMLResponse)
async def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_token(token, credentials_exception)
    if user and not user.is_verified:
        user.is_verified = True   
        verify_user = db.query(models.Users).filter(models.Users.id == user.id)
        verify_user.update({'is_verified': user.is_verified}, synchronize_session=False)
        db.commit()
        print("worked")
        return templates.TemplateResponse('verification.html',
                                        {"request": request,
                                        "username": user.username})

    raise credentials_exception

@router.post('/login', status_code=status.HTTP_200_OK,
            response_model=SignInResponse)
async def login(user:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)): 
    user_cred = db.query(models.Users).filter(models.Users.email==user.username).first()
    
    if user_cred.is_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='email not verified')
    if not user_cred:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid email or password')
    hashed_pwd = verify_pwd(user.password, user_cred.password) 
    if not hashed_pwd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid email or password')
    
    data = {
        'user_id': user_cred.id,
        'is_super': user_cred.is_superuser,
        'is_admin': user_cred.is_admin,
        'is_verified': user_cred.is_verified
    }
    access_token = create_access_token(data)
    return {'token': access_token, 'token_type': "Bearer"}