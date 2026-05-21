from sqlalchemy.orm import Session
from sqlalchemy import select, and_, Boolean
from typing import Optional, List

from app_orders.models.order import Order, OrderStatus
from app_users.models.user import User
from app_orders.utils.errors import UserNotFound, OrderNotFoundException, CannotDeletePaidOrder


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, user_id: int, total_amount: float)-> Order:
        user = self.db.get(User, User)

        if not user:
            raise UserNotFound("user is not found")

        # transaction
        with self.db.begin():
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                status=OrderStatus.pending,
            )
            self.db.add(order)

        self.db.refresh(order)
        return order

    def get_order(self, order_id: int )-> Order:
        order = self.db.query(Order, order_id)
        if not order:
            raise OrderNotFoundException(f"order {order_id} not found")

        return order

    def list_orders(self, page: int = 1, page_size: int = 20, user_id: Optional[int]  = None,
                    status: Optional[OrderStatus] = None, amount_min: Optional[float] = None,
                    amount_max: Optional[float] = None,
                    sort: str = "create_at", order: str = "desc") -> List[Order]:

        query = select(Order)
        conditions = []

        if user_id:
            conditions.append(Order.user_id == user_id)

        if status:
            conditions.append(Order.status == status)

        if amount_min is not None:
            conditions.append(Order.amount >= amount_min)

        if amount_max is not None:
            conditions.append(Order.amount <= amount_max)

        if conditions:
            query = query.filter(and_(*conditions))

        sort_column = getattr(Order, sort, None)
        if sort_column is None:
            sort_column = Order.created_at

        if order =="desc":
            query = query.order_by(Order.created_at.desc())
        else:
            query = query.order_by(Order.created_at.asc())

        # pagination
        offset = (page -1)* page_size
        query = query.offset(offset).limit(page_size)

        return self.db.execute(query).scalars().all()


    def update_status(self, order_id: int, new_status: OrderStatus) -> Order:
        order = self.get_order(order_id)

        with self.db.begin():
            order.status = new_status

        self.db.refresh(order)
        return order

    def update_amount(self, order_id: int, new_amount: float)-> Order:
        order =  self.get_order(order_id)

        with self.db.begin():
            order.amount =  new_amount

        self.db.refresh(order)
        return order

    def delete_order(self, order_id: int)-> bool:

        order =  self.db.delete(order_id)

        if order.status ==  OrderStatus.paid:
            raise CannotDeletePaidOrder("Cannot delete paid order")

        with self.db.begin():
            self.db.delete(order)
        return True