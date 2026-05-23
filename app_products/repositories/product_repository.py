from math import prod

from sqlalchemy.ext.asyncio import result
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from app_products.models.product import Product
from app_products.utils.errors import ProductNameExists, ProductNotFound


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, name: str, category: str, price: float, in_stock: bool):
        product = Product(
            name=name,
            category=category,
            price=price,
            in_stock=in_stock,
        )
        try:
            with self.db.begin():
                self.db.add(product)
        except IntegrityError:
            raise ProductNameExists(f"product with name {name} already exists")

        self.db.refresh(product)
        return product

    def get_product(self, product_id: int)-> Product:
        product = self.db.query(Product, product_id)
        if not product:
            raise ProductNotFound(f"product with id {product_id} not found")
        return product

    def list_product(self, page: int = 1, page_size: int = 20, name:Optional[str]=None,
                     category:Optional[str]=None,price_min:Optional[float]=None,
                     price_max:Optional[float]=None,in_stock:Optional[bool]=None,
                     sort:str = "created_at", order:str="desc") -> List[Product]:

        query = self.db.query(Product)
        conditions = []

        if name:
            conditions.append(Product.name.ilike(f"%{name}%"))

        if category:
            conditions.append(Product.category==category)
        if price_min is not None:
            conditions.append(Product.price>=price_min)
        if price_max is not None:
            conditions.append(Product.price<=price_max)
        if in_stock is not None:
            conditions.append(Product.in_stock==in_stock)

        if conditions:
            query = query.where(and_(*conditions))
        if sort == "price":
            sort_column = Product.price
        else:
            sort_column = Product.created_at

        if order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = self.db.execute(query).scalars().all()
        return result

    #Put
    def update_product(self, product_id: int, name: str, category:str, price: float,
                       in_stock: bool) -> Product:

        product = self.get_product( product_id)
        product.name = name
        product.category = category
        product.price = price
        product.in_stock = in_stock

        try:
            with self.db.begin():
                self.db.add(product)
        except IntegrityError:
            raise ProductNameExists(f"product with name {name} already exists")
        self.db.refresh(product)
        return product


    def patch_product(self, product_id: int, name: str, category: str, price: float,
                      in_stock: bool) -> Product:
        product =  self.get_product(product_id)

        if name is not None:
            product.name = name
        if category is not None:
            product.category = category
        if price is not None:
            product.price = price
        if in_stock is not None:
            product.in_stock = in_stock

        try:
            with self.db.begin():
                self.db.add(product)
        except IntegrityError:
            raise ProductNameExists(f" product with name {name} already exists")

        self.db.refresh(product)
        return product


    def delete_product(self, product_id: int)-> bool:
        product = self.get_product(product_id)

        with self.db.begin():
            self.db.delete(product)
        return True