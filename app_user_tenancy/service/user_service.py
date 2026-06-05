from fastapi import HTTPException
from app_user_tenancy.models.users import User
from app_user_tenancy.repositories.user_repository import UserRepository
from app_user_tenancy.schemas.user import UserRead, UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository



    def get_user(self, user_id: int) -> UserRead:
        user = self.repository.get(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserRead(id=user.id, full_name=user.full_name, email=user.email,
                        created_at=user.created_at, marketing_opt_in=user.marketing_opt_in)

    def create_user(self, user: UserCreate) -> UserRead:
        user = User(
            tenant_id=self.repository.tenant_id,
            full_name=user.full_name,
            email=user.email,
        )
        user = self.repository.create_user(user)
        return self.get_user(user.id)

    def update_user(self,user_id: int,  payload: UserUpdate) -> UserRead:
        user = self.repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in payload.dict(exclude_none=True).items():
            setattr(user, key, value)

        self.repository.save_user(user)
        return self.get_user(user.id)


    def delete_user(self,user_id: int):
        user = self.repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.repository.delete_user(user)
