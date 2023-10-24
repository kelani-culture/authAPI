from passlib.context import CryptContext
import re


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_pwd(plain_pass, hash_pass):
   return pwd_context.verify(plain_pass, hash_pass) 

def hash_password(password):
    return pwd_context.hash(password)