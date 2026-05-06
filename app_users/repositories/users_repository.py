from psycopg2.errorcodes import CLASS_INVALID_SQL_STATEMENT_NAME
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

from app_users.models import user
from app_users.models.user import User
from app_users.utils.errors import UserNotFound
from typing import Optional, List


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self,email: str, first_name: str,last_name: str, age: Optional[int] ):
        user = User(email=email, first_name=first_name, last_name=last_name, age=age)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int):
        user  = self.db.get(User, user_id)
        if not user:
            raise UserNotFound(f"user with id {user_id} not found")
        return user


    def list_users(self, page: int = 1, page_size: int =20,  email: Optional[str] = None,
                   first_name: Optional[str] = None, last_name:Optional[str] = None,
                   age_min: Optional[int] = None, age_max: Optional[int] = None,
                   sort: str = 'created_at', order: str = 'desc'):
        query =  select(User)
        condition  = []
        if email:
            condition.append(User.email == email)
        if first_name:
            condition.append(User.first_name == first_name)

        if last_name:
            condition.append(User.last_name == last_name)

        if age_max is not None:
            condition.append(User.age <= age_max)

        if age_min is not None:
            condition.append(User.age >= age_min)

        if sort  == "email":
            sort_column = User.email
        else:
            sort_column = User.created_at
        if order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        offset  = (page - 1) * page_size
        query  = query.offset(offset).limit(page_size)

        return self.db.execute(query).scalars().all()

    # put
    def update_user(self, user_id: int, email: str, first_name: str, last_name: str,
                    age: Optional[int]):
        user = self.get_user(user_id)

        user.email = email
        user.first_name =  first_name
        user.last_name = last_name
        user.age = age = age

        self.db.commit()
        self.db.refresh(user)
        return user

    #patch
    def partial_update_user(self, user_id: int, email: str, first_name: str, last_name: str,
                            age: Optional[int]):
        user = self.get_user(user_id)

        if email is not None:
            user.email = email

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if age is not None:
            user.age = age

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
        return True