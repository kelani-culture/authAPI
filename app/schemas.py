from pydantic import (BaseModel, EmailStr, Field, validator,
                      model_validator) 
from datetime  import datetime
import re

"""
shcemas for our application
"""
name_regex = "^[a-zA-Z]+$"
# Minimum eight characters, at least one uppercase letter,
# one lowercase letter, one number and one special character:
pass_regex ="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
phone_regex="^[0-9]+$"
 

class UserSignUp(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)

    @validator('first_name', 'last_name')
    def validate_name(cls, name):
        match = re.match(name_regex, name)
        if not match:
            raise ValueError('first name and lastname '+\
                'must contain letters only')
        return name

    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @model_validator(mode='after')
    def validate_password(self):
        pwd1 = self.password
        pwd2 = self.confirm_password
        
        if not re.match(pass_regex, pwd1):
            raise ValueError('password not strong enough')
        
        if (not pwd1 and not pwd2) or (pwd1 != pwd2):
            raise ValueError('passwords do not match')

        return self
     
    phone_number: str = Field(min_length=11)
    @validator('phone_number')
    def validate_number(cls, num):
        match = re.match(phone_regex, num)
        if not match:
            raise ValueError('Invalid phone number')
        return num


class UserSignUpResponse(BaseModel):
    message: str = Field(default='User created successfully') 
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime

    class Config:
        orm_mode = True


class SignIn(BaseModel):
    email: EmailStr
    password: str

class SignInResponse(BaseModel):
    token: str
    token_type: str