from typing import List
from fastapi import (APIRouter, Response, status,
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
    #get and return all product
    prod = db.query(models.Product).all()
    return prod

    
@router.put('/product/{id}', status_code=status.HTTP_200_OK,
            response_model=ProductResponse)
def update_product(id: int, product: Product, db: Session= Depends(get_db),
                   user = Depends(get_current_user)):
    if user.is_admin is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User not an admin cannot update product')
    update_prod = db.query(models.Product).filter(models.Product.id == id)
    prod = update_prod.first()
    if prod is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"product with id of {id} not found") 
    if prod.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='user not allowed to modify products')
    print(product)
    update_prod.update(product.dict(), synchronize_session=False)
    db.commit()
    return {"message":"product updated successfully", "products":prod}


@router.delete('/product/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int, db:Session = Depends(get_db),
                   user = Depends(get_current_user)):
    if user.is_admin is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized user")
    delete_prod = db.query(models.Product).filter(models.Product.id == id)
    delete = delete_prod.first()
    if delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id {id} does not exist")
    
    if delete.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Unauthorized user is forbidden from deleting product")
    delete_prod.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)