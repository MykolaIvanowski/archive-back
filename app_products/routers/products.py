from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from starlette import status

from app_products.db.database import SessionLocal, get_db
from app_products.services.product_service import (
    ProductService,
    InvalidProductData,
)
from app_products.repositories.product_repository import (
    ProductNotFound,
    ProductNameExists,
)
from app_products.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
    ProductPatch,
)


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductRead])
def create_product(payload: ProductCreate, db : Session = Depends(get_db))->ProductRead:
    service = ProductService(db)

    try:
        return service.create_product(
            name=payload.name,
            category=payload.category,
            price=payload.price,
            in_stock=payload.in_stock,
        )
    except InvalidProductData as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNameExists as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=ProductRead)
def get_product(product_id: int, db : Session = Depends(get_db))->ProductRead:
    service = ProductService(db=db)
    try:
        return service.create_product(product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[ProductRead])
def product_list(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                 name: Optional[str]= None, category: Optional[str]= None,
                 price_min: Optional[float]= None, price_max: Optional[float]= None,in_stock: bool = None,
                 sort:str = Query("create_at", reegx="^(create_at|price)$"),
                 order: str = Query("desc", regex="^(asc|desc)$"), db : Session = Depends(get_db)
                 ) -> List[ProductRead]:
    service = ProductService(db=db)
    return service.list_products(
        page=page,
        page_siza=page_size,
        name=name,
        category=category,
        price_min=price_min,
        price_max=price_max,
        in_stock=in_stock,
        sort=sort,
        order=order,

    )

@router.put("/{product_id", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db : Session = Depends(get_db)):
    service = ProductService(db=db)
    try:
        return service.update_product(product_id, name=payload.name, category=payload.category, price=payload.price,
                                      in_stock=payload.in_stock)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail="product not found")
    except ProductNameExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidProductData as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{product_id}", response_model=ProductRead)
def patch_product(product_id: int, payload: ProductPatch, db : Session = Depends(get_db)):
    service = ProductService(db=db)
    try:
        return service.patch_product(product_id, name=payload.name, category=payload.category, price=payload.price,
                                     in_stock=payload.in_stock)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail="product not found")
    except ProductNameExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidProductData as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db : Session = Depends(get_db)):
    service = ProductService(db=db)

    try:
        return service.delete_product(product_id)
    except ProductNotFound :
        raise HTTPException(status_code=404, detail="product not found")