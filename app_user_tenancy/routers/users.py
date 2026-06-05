from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status

from app_user_tenancy.db.database import get_db
from app_user_tenancy.repositories.user_repository import UserRepository
from app_user_tenancy.service.user_service import UserService
from app_user_tenancy.schemas.user import UserCreate, UserUpdate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


def get_service(request: Request, db: Session = Depends(get_db)):
    repository = UserRepository(db=db, tenant_id=request.state.tenant_id)
    return UserService(repository)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(Payload: UserCreate, service: UserService = Depends(get_service)):
    return service.create_user(Payload)

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user(user_id: int, service: UserService = Depends(get_service) ):
    return service.get_user(user_id)

@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(user_id: int, payload: UserUpdate, service: UserService = Depends(get_service)):
    return service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    service.delete_user(user_id)