from logging import exception

from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from app_orders.utils.errors import IdempotencyKeyNotFound, IdempotencyKeyConflict
from app_orders.models.order import Order
from app_orders.models.idempotency_key import IdempotencyKey


class IdempotencyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_key(self, key: int) -> Optional[IdempotencyKey]:
        stmt = select(IdempotencyKey).where(IdempotencyKey.key == key)
        return self.db.execute(stmt).scalar_one_or_none()


    def create_key(self, key: int) -> IdempotencyKey:
        idem = IdempotencyKey(key=key, status='processing')
        try:
            with self.db.begin():
                self.db.add(idem)
        except Exception:
            raise IdempotencyKeyConflict(f" key {key} already exists")
        return idem

    def save_response(self, key: str, response: dict, order_id: int):
        idem = self.get_key(key)
        if not idem:
            raise IdempotencyKeyNotFound(f" key {key} not found")

        idem.status = 'completed'
        idem.response = response
        idem.order_id = order_id


        with self.db.begin():
            self.db.add(idem)
