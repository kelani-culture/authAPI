from typing import List
from fastapi import (APIRouter, status,
                     Depends, HTTPException)
from ..database import get_db
from .. import models
from ..schemas import Product, ProductResponse, GetProduct
from ..oauth import get_current_user
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['products']
)


@router.post('/create-products', status_code=status.HTTP_201_CREATED,
             response_model=ProductResponse)
def create_product(prod: Product, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_admin is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='unauthorized User')
    prod_dict = prod.dict()
    prod_dict.update({'user_id': current_user.id})
    to_prod = models.Product(**prod_dict)
    db.add(to_prod)
    db.commit()
    db.refresh(to_prod)
    return {'message': 'product created successfully', 'products': to_prod}




@router.get('/products', status_code=status.HTTP_200_OK,
            response_model=List[GetProduct])
def get_product(db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    prod = db.query(models.Product).all()
    return prod