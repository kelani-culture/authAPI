from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_username: str
    db_password: str
    db_port: str
    db_host: str
    
    class Config:
        env_file = '.env'

settings = Settings()    