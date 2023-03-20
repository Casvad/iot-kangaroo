from repositories.base_repository import SessionLocal
from repositories.models.dbuser import DBUser, DBDevice


class DeviceRepository:

    def __init__(self, db: SessionLocal):
        self.db = db

    def create_device(self, device: DBDevice):
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update_device(self, device: DBDevice):
        device_query = self.db.query(DBDevice).filter(DBDevice.id == device.id)
        device_query.update(device.dict(exclude_unset=True), synchronize_session=False)
        self.db.commit()
        self.db.refresh(device)

        return device

    def find_by_email(self, email):
        return self.db.query(DBDevice).filter(DBDevice.email == email).all()

    def find_by_device_id(self, device_id):
        return self.db.query(DBDevice).filter(DBDevice.id == device_id).first()
