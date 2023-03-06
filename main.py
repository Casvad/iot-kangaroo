from datetime import timedelta

from fastapi import FastAPI
from fastapi_login import LoginManager
from fastapi import Depends

from models.device import Device
from models.user import User
from services.device_service import DeviceService
from services.user_service import UserService

app = FastAPI()
SECRET = "c7cc52d136f38be8e8e50b3efa5a828dc699726ff1f870c1"
manager = LoginManager(SECRET, token_url='/auth/token')
userService = UserService()
deviceService = DeviceService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users")
def users_create_user(user: User):
    return userService.create_user(user)


@app.post('/users/login')
def login(data: User):
    email = data.email
    password = data.password

    userService.login_user(email, password)
    access_token = manager.create_access_token(data=dict(sub=email), expires=timedelta(days=120))
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/users")
def users_detail(user=Depends(manager)):
    user = userService.user_detail(user.email)
    return user


@app.post("/devices")
def devices_register(device: Device, user=Depends(manager)):
    return deviceService.create_device_for_user(user.email, device)


@app.get("/devices")
def devices_detail(user=Depends(manager)):
    return deviceService.list_devices(user.email)


@manager.user_loader()
def load_user(email: str):
    user = userService.user_detail(email)
    return user
