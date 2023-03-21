from models.device import Device
from repositories.base_repository import get_db
from repositories.device_repository import DeviceRepository
from repositories.models.dbuser import DBDevice
from services.infura_web3 import Web3Service
from utils.rsa_gen import generate_keys


class DeviceService:

    def __init__(self):
        self.device_repository = DeviceRepository(lambda: get_db())
        self.web3Service = Web3Service(self)

    def get_keys(self):
        x = generate_keys()

        return x

    def create_device_for_user(self, email, device: Device):
        user_devices = self.device_repository.find_by_email(email)

        if user_devices is None:
            user_devices = []
        keys = generate_keys()

        user_devices.append(device)
        db_device = DBDevice()
        db_device.id = device.id
        db_device.user_email = email

        transaction_address = self.web3Service.create_digital_twin(device.id, keys['jwk']['n'])
        self.device_repository.create_device(db_device)
        keys["web3_transaction"] = transaction_address
        return db_device

    def device_transaction(self, email, device):
        return self.web3Service.create_transaction(device.address, device.signature, device.data)

    def join_digital_twin(self, device_id, device_address):
        clean_device_id = str(device_id).replace("b'", "").replace("'", "")
        device = self.device_repository.find_by_device_id(clean_device_id)
        if device is not None:
            device.digitalTwin = device_address
            self.device_repository.update_device(device)

    def list_devices(self, email):
        return self.device_repository.find_by_email(email)
