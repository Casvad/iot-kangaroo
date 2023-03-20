from repositories.base_repository import SessionLocal
from repositories.models.dbuser import DBUser


class UserRepository:

    def __init__(self, db: SessionLocal):
        self.db = db

    def create_user(self, user: DBUser):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def find_by_email(self, email):
        return self.db.query(DBUser).filter(DBUser.email == email).first()
