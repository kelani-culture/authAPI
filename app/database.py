from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

"""
this file setup sql alchemy orm connecting it to the database
"""
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.db_username}:{settings.db_password}@'+\
                       f'{settings.db_host}:{settings.db_port}/{settings.db_name}'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()