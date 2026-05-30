from sqlalchemy.orm import Session
from typing import Optional, List

from app_orders.repositories.orders_repository import OrderRepository
from app_orders.utils.errors import OrderNotFoundException, UserNotFound, InvalidStatusTransition, CannotModifyPaidOrder
from app_users.repositories.users_repository import UsersRepository
from app_orders.models.order import OrderStatus, Order


class OrdersService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = OrderRepository(db)
        self.user_repository = UsersRepository(db)


    def create_order(self, user_id: int, total_amount: float, metadata: dict,amount: int, product: str )-> Order:
        if total_amount <= 0:
            raise ValueError(f"total amount must be grater than 0")

        return self.repository.create_order(
            user_id=user_id,
            total_amount=total_amount,
            metadata=metadata,
            amount=amount,
            product=product,
        )
    def get_order(self, order_id: int)-> Order:
        return self.repository.get_order(order_id)

    def list_orders(self,  page: int, page_size: int, user_id: Optional[int]=None,
                    status: Optional[OrderStatus] =None, amount_max:Optional[float]  = None,
                    amount_min:Optional[float] = None, sort: str = "create_at", order:str = "desc") -> List[Order]:
        return self.repository.list_orders(
            page=page,
            page_size=page_size,
            user_id=user_id,
            status=status,
            amount_max=amount_max,
            amount_min=amount_min,
            sort=sort,
            order=order
        )

    def update_status(self, order_id: int, new_status: OrderStatus)-> Order:
        order = self.repository.get_order(order_id)

        if order.status == OrderStatus.paid and new_status ==OrderStatus.pending:
            raise InvalidStatusTransition("Cannot revert paid to pending status")

        if order.status != OrderStatus.pending and new_status == OrderStatus.canceled:
            raise InvalidStatusTransition("Cannot cancel a paid status order")

        return self.repository.update_status(order_id, new_status)


    def update_amount(self, order_id: int, new_amount: float)-> Order:
        if new_amount <= 0:
            raise ValueError("Total amount must be greater than 0")

        order = self.repository.get_order(order_id)

        if order.status == OrderStatus.paid:
            raise CannotModifyPaidOrder("Cannot modify paid order")

        return self.repository.update_amount(order_id, new_amount)

    def delete_order(self, order_id: int)->bool:
        order = self.repository.get_order(order_id)

        if order.status == OrderStatus.paid:
            raise  CannotModifyPaidOrder("Cannot delete  a paid order")

        return self.repository.delete_order(order_id)