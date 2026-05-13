from sqlalchemy.orm import Session, query
from app_users.repositories.users_repository import UsersRepository
from app_users.utils.errors import UserNotFound
from app_users.models.user import User
from typing import Optional, List
from app_users.utils.errors import EmailAlreadyExists


class UsersService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UsersRepository(db)

    def _get_by_email(self, email: str) -> Optional[str]:
        query = self.db.query(User).filter(User.email == email).first()
        return query


    def create_user(self, email:str, first_name: str, last_name: str,
                    age: Optional[int]) -> User:
        existing = self._get_by_email(email)
        if existing:
            raise EmailAlreadyExists(f'Email name already exists for {email}')
        return self.repository.create_user(email=email, first_name=first_name,
                                           last_name=last_name, age=age)

    def get_user(self, user_id: int)-> User:
        return self.repository.create_user(user_id)

    def list_users(self, page: int = 1,page_size: int  = 20, email: Optional[str] = None,
                   first_name: Optional[str] = None, last_name: Optional[str] =  None,
                   age_min: Optional[int]= None, age_max: Optional[int] = None,
                   sort: str = 'created_at', order: str = 'desc')-> List[User]:

        return self.repository.list_users(page =page, page_size=page_size, email=email,
                                          first_name=first_name, last_name=last_name,
                                          age_min=age_min, age_max=age_max, sort=sort,
                                           order=order)



    def update_user(self, user_id: int, email: str,  first_name: str, last_name:str,
                    age: Optional[int])-> User:
        existing  = self._get_by_email(email)
        if existing and existing.id != user_id:
            raise EmailAlreadyExists(f'email already exists for name {email}')

        return self.repository.update_user( user_id=user_id, email=email, first_name=first_name,
                                            last_name=last_name, age=age)


    def partial_update_user(self, user_id: int, email: Optional[str] = None, first_name: Optional[str] = None,
                            last_name: Optional[str] = None, age: Optional[int] = None)-> User:
        if email is not None:
            existing = self._get_by_email(email)
            if existing and existing.id != user_id:
                raise EmailAlreadyExists(f'email already exists for name {email}')

        return self.repository.partial_update_user(user_id=user_id, email=email, first_name=first_name,
                                                   last_name=last_name, age=age)

    def delete_user(self, user_id: int)-> Optional[User]:
        return self.repository.delete_user(user_id=user_id)

