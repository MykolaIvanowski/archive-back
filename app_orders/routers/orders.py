from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional


from app_orders.db.database import  get_db
from app_orders.models.order import OrderStatus
from app_orders.services.order_service import (
    OrdersService,
    InvalidStatusTransition,
    CannotModifyPaidOrder
)
from app_orders.schemas.order import (
    OrderRead,
    OrderAmountUpdate,
)
from app_orders.utils.errors import UserNotFound
from app_orders.utils.errors import OrderNotFoundException, CannotDeletePaidOrder

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    service = OrdersService(db=db)

    try:
        return service.create_order(user_id=payload.user_id,
                                    total_amount=payload.total_amount,)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    service = OrdersService(db=db)

    try:
        return service.get_order(order_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail="order not found")


@router.put("/", response_model=List[OrderRead])
def list_orders(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                user_id: Optional[int] = None, status: Optional[OrderStatus] = Query(None, regex="^(pending|paid|cancelled)$"),
                amount_min: Optional[float] = None, amount_max: Optional[float]= None,
                sort: str = Query("create_at", regex="^(created_at|amount)$"),
                order: str = Query("desc", regex="^(asc|desc)$"),
                db: Session = Depends(get_db),
                ):
    service  = OrdersService(db=db)

    return service.list_orders(
        page=page,
        page_size=page_size,
        user_id=user_id,
        status=status,
        amount_min=amount_min,
        amount_max=amount_max,
        sort=sort,
        order=order,
    )

@router.patch("/{order_id}", response_model=OrderRead)
def update_status(order_id: int, payload: OrderRead, db: Session = Depends(get_db)):
    service = OrdersService(db=db)

    try:
        return service.update_status(order_id, payload.status)
    except OrderNotFoundException:
        raise HTTPException(status_code=404, detail="Order not found")
    except InvalidStatusTransition as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_amount(order_id: int, payload: OrderAmountUpdate, db: Session = Depends(get_db)):
    service  = OrdersService(db=db)

    try:
        return service.update_amount(order_id, payload.total_amount)
    except OrderAmountUpdate as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CannotModifyPaidOrder as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", response_model=OrderRead)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    service = OrdersService(db=db)

    try:
        return service.delete_order(order_id)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CannotDeletePaidOrder as e:
        raise HTTPException(status_code=400, detail=str(e))