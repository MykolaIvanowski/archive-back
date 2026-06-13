from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from  app_users.db.database import get_db
from app_users.services.users_service import UsersService, EmailAlreadyExists
from app_users.schemas.user_v2 import (
    UserCreateV2,
    UserReadV2,
    UserUpdateV2,
    UserPatchV2,
)

router = APIRouter(prefix="/v2/users", tags=["users-v2"])
router.version = "v2"

@router.post("/", response_model=UserReadV2, tags=["users"])
def create_user_v2(payload: UserCreateV2, db: Session = Depends(get_db)):
    service  =  UsersService(db=db)

    try:
        user = service.create_user_v2(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            age=payload.age
        )
        return user
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id", response_model=UserReadV2)
def get_user_v2(user_id: int, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.get_user_v2(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")



@router.get("/", response_model=List[UserReadV2])
def list_user_v2(page: int = Query(1, ge=1),
              page_size: int =Query(20, ge=1, le=100),
              email: Optional[str] = None, first_name: Optional[str]= None,
              last_name: Optional[str]= None, age_min: Optional[int] = None,
              age_max: Optional[int]= None,
              sort: str = Query("created_at", regex="^(email|created_at$)"),
              order: str = Query("desc", regex="asc|desc"),
              db: Session = Depends(get_db)):

    service = UsersService(db)
    return service.list_users_v2(
        page=page, page_size=page_size, email=email, first_name=first_name,
        last_name=last_name, age_min=age_min, age_max=age_max, sort=sort,
        order=order
    )

@router.put("/{user_id}", response_model=UserReadV2)
def update_user_v2(user_id: int, payload: UserUpdateV2, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.update_user_v2(
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


@router.patch("/{user_id}", response_model=UserReadV2)
def partial_update_v2(user_id: int, payload: UserPatchV2, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        return service.partial_update_user_v2(user_id=user_id, email=payload.email,
                                           first_name=payload.first_name,
                                           last_name=payload.last_name,
                                           age=payload.age)
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=404, detail='User not found')


@router.delete(" /{user_id}", status_code=204)
def delete_user_v2(user_id: int, db: Session = Depends(get_db)):
    service = UsersService(db=db)

    try:
        service.delete_user(user_id, version=router.version) # simple version in case versioning required change
                                                             # only in bussines logic
        return
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")