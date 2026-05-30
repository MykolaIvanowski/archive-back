from sqlalchemy.orm import Session

from app_orders.repositories.idempotency_repository import (
    IdempotencyRepository,
    IdempotencyKeyConflict,
)
from app_orders.models.order import  Order
from app_orders.services.order_service import OrdersService


class IdempotentService:
    def __init__(self, db: Session):
        self.db = db
        self.orders_service = OrdersService(db=db)
        self.idempotency_repository = IdempotencyRepository(db)
    def create_order(self, key: str,user_id: int,  product: str, amount: int, metadata: dict, total_amount:int) -> Order:
        existing =  self.idempotency_repository.get_key(key)
        if existing:
            if existing.status == "completed":
                return existing.status
            if existing.status == "processing":
                return {"status": "processing"}

        try:
            self.idempotency_repository.create_key(key)
        except IdempotencyKeyConflict:
            existing = self.orders_repository.get_key(key=key)
            return self.responce if existing.status == "completed" else {"status": "processing"}

        order = self.orders_service.create_order(
            user_id=user_id,
            product=product,
            amount=amount,
            metadata=metadata,
            total_amount=total_amount
        )

        response = {
            "order_id": order.order_id,
            "order": order.order,
            "metadata": order.metadata,
            "total_amount": order.total_amount,
            "amount": order.amount,
        }

        self.idempotency_repository.save_response(
            key=key,response=response, order_id=order.order_id
        )
        return response