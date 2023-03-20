from models.device import Device
from services.infura_web3 import Web3Service
from utils.rsa_gen import generate_keys


class DeviceService:

    def __init__(self):
        self.devices = {}
        self.web3Service = Web3Service(self)

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

        transaction_address = self.web3Service.create_digital_twin(device.id, keys['jwk']['n'])
        keys["web3_transaction"] = transaction_address
        return keys

    def device_transaction(self, email, device):
        return self.web3Service.create_transaction(device.address, device.signature, device.data)

    def join_digital_twin(self, device_id, device_address):
        user_devices = self.devices.get("carlos@sumerlabs.com")
        clean_device_id = str(device_id).replace("b'", "").replace("'", "")
        device = next((i for i in user_devices if i.id == clean_device_id), None)
        if device is not None:
            device.digitalTwin = device_address

    def list_devices(self, email):
        return self.devices[email]
