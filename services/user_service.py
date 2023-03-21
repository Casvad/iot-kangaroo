from models.user import User
from repositories.base_repository import get_db
from repositories.models.dbuser import DBUser
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        # This could be injected in controller as db: Session = Depends(get_db)
        self.user_repository = UserRepository(lambda: get_db())

    def create_user(self, user: User):
        db_user = DBUser()
        db_user.id = user.id
        db_user.email = user.email
        db_user.password = user.password

        self.user_repository.create_user(db_user)

        return db_user

    def login_user(self, email, password):

        user = self.user_repository.find_by_email(email)
        if user is None:
            raise "user not found"
        elif user.password != password:
            raise "user bad password"
        return user

    def user_detail(self, email):
        user = self.user_repository.find_by_email(email)
        if user is None:
            raise "user not found"
        return user
