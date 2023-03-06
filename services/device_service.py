from models.device import Device
from utils.rsa_gen import generate_keys


class DeviceService:

    def __init__(self):
        self.devices = {}

    def get_keys(self):
        x = generate_keys()

        return x

    def create_device_for_user(self, email, device: Device):
        user_devices = self.devices.get(email)

        if user_devices is None:
            user_devices = []
        keys = generate_keys()

        user_devices.append(device)
        self.devices[email] = user_devices
        return keys

    def list_devices(self, email):
        return self.devices[email]
