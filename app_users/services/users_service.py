from sqlalchemy.orm import Session, query
from app_users.repositories.users_repository import UsersRepository
from app_users.utils.errors import UserNotFound
from app_users.models.user import User
from typing import Optional, List


class UserService:
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

class EmailAlreadyExists(Exception):
    pass

