from sqlalchemy.orm import Session
from app_user_tenancy.models.users import User


class UserRepository:
    def __init__(self, db: Session, tenant_id : str):
        self.db = db
        self.tenant_id = tenant_id


    def get(self, user_id: int) :
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.tenant_id == self.tenant_id,
                    User.deleted == False).first()
        )

    def list(self):
        return (
            self.db.query(User)
            .filter(User.deleted == False, User.tenant_id == self.tenant_id)
            .all()
        )

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        user.deleted = True
        self.save_user(user)
