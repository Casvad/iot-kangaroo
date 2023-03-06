class UserService:

    def __init__(self):
        self.users = {}

    def create_user(self, user):
        self.users[user.email] = user

        return user

    def login_user(self, email, password):

        user = self.users[email]
        if user is None:
            raise "user not found"
        elif user.password != password:
            raise "user bad password"
        return user

    def user_detail(self, email):
        user = self.users[email]
        if user is None:
            raise "user not found"
        return user
