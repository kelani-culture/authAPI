from  fastapi import FastAPI
from .database import engine
from . import models
from .views import authenticate, root, products

models.Base.metadata.create_all(bind=engine)

print('connected')
app = FastAPI()

app.include_router(authenticate.router)
app.include_router(root.router)
app.include_router(products.router)