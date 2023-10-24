from  fastapi import FastAPI
from .database import engine
from . import models
from .views import authenticate

models.Base.metadata.create_all(bind=engine)

print('connected')
app = FastAPI()

app.include_router(authenticate.router)