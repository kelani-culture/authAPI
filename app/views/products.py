from fastapi import (APIRouter, status,
                     Depends, HTTPException)
from ..database import get_db
from .. import models, schemas
from ..oauth import get_current_user

router = APIRouter(
    tags=['products']
)

@router.get('/products')
def get_product(current_user: int = Depends(get_current_user)):
    return {'message': 'authenticated user'}