from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app_users.db.database import SessionLocal
from app_users.services.users_service import UsersService, EmailAlreadyExists
from app_users.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserPatch,
)

router  =  APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", responce_model=UserRead, tags=["users"])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    service  =  UsersService(db=db)

    try:
        user = service.create_user(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            age=payload.age
        )
        return user
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.get_user(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")



@router.get("/", response_model=List[UserRead])
def list_user(page: int = Query(1, ge=1),
              page_size: int =Query(20, ge=1, le=100),
              email: Optional[str] = None, first_name: Optional[str]= None,
              last_name: Optional[str]= None, age_min: Optional[int] = None,
              age_max: Optional[int]= None,
              sort: str = Query("created_at", regex="^(email|created_at$)"),
              order: str = Query("desc", regex="asc|desc"),
              db: Session = Depends(get_db)):

    service = UsersService(db)
    return service.list_users(
        page=page, page_size=page_size, email=email, first_name=first_name,
        last_name=last_name, age_min=age_min, age_max=age_max, sort=sort,
        order=order
    )

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.update_user(
            user_id=user_id,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            age=payload.age
        )
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/{user_id}", response_model=UserRead)
def partial_update(user_id: int, payload: UserPatch, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.partial_update_user(user_id=user_id, email=payload.email,
                                           first_name=payload.first_name,
                                           last_name=payload.last_name,
                                           age=payload.age)
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        service.delete_user(user_id)
        return
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
