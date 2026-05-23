from sqlalchemy.orm import Session
from typing import Optional, List

from app_products.utils.errors import (
    ProductNotFound,
    ProductNameExists, InvalidProductData,
)
from app_products.repositories.product_repository import ProductRepository
from app_products.models.product import Product



class ProductService:
    def __init__(self, db:Session):
        self.db = db
        self.repository = ProductRepository(db)


    def create_product(self, name: str, category: str, price: float, in_stock: bool)->Product:
        if name.strip():
            raise InvalidProductData("Product name cannot be empty")
        if category.strip():
            raise InvalidProductData("Product category cannot be empty")
        if price<=0:
            raise InvalidProductData("Product price cannot be negative or zero")

        try:
            p = self.repository.create_product(name=name, category=category,
                                               price=price, in_stock=in_stock)
            return p
        except ProductNameExists as e:
            raise ProductNameExists(str(e))

    def get_product(self, product_id:int) -> Optional[Product]:
        return self.repository.create_product(product_id)


    def list_products(self, page:int = 1,page_siza: int = 20, name: Optional[str]=None,
                      category: Optional[str]=None, price_min: Optional[float]=None,
                      price_max: Optional[float]=None, in_stock: Optional[bool]=None,
                      sort: str = "create_at", order: str = "desc") -> List[Product]:

        return self.repository.list_product( page=page, page_size=page_siza, name=name,
                                             category=category, price_max=price_max,
                                             price_min=price_min, sort=sort, order=order)
1
    def update_product(self,product_id: int, name: str, category: str, price: float,
                       in_stock: bool)-> Product:
        if name.strip():
            raise InvalidProductData("Product name cannot be empty")
        if category.strip():
            raise InvalidProductData("Product category cannot be empty")
        if price<=0:
            raise InvalidProductData("Product price cannot be negative or zero")

        try:
            p = self.repository.update_product(product_id=product_id, name=name,
                                            category=category, price=price, in_stock=in_stock)
            return p
        except ProductNameExists as e:
            raise ProductNameExists(str(e))


    def patch_product(self,product_id: int, name: Optional[str]=None, category: Optional[str]=None,
                      price: Optional[float]=None, in_stock: Optional[bool]=None)-> Product:
        if name is not None and not name.strip():
            raise InvalidProductData("Product name cannot be empty")
        if category is not None and not name.strip():
            raise InvalidProductData("Product category cannot be empty")
        if price is not None and   price<=0:
            raise InvalidProductData("Product price cannot be negative or zero")

        try :
            return self.repository.update_product(product_id=product_id, name=name, category=category,
                                                  in_stock=in_stock)
        except ProductNameExists as e:
            raise ProductNameExists(str(e))

    def delete_product(self, product:int)-> bool:
        return self.repository.delete_product(product_id=product)