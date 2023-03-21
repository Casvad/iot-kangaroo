from repositories.base_repository import SessionLocal
from repositories.models.dbuser import DBUser, DBDevice


class DeviceRepository:

    def __init__(self, db: SessionLocal):
        self.db = db

    def create_device(self, device: DBDevice):
        db = next(self.db())
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def update_device(self, device: DBDevice):
        db = next(self.db())
        device_query = db.query(DBDevice).filter(DBDevice.id == device.id)
        device_query.update(device.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        db.refresh(device)

        return device

    def find_by_email(self, email):
        db = next(self.db())
        return db.query(DBDevice).filter(DBDevice.user_email == email).all()

    def find_by_device_id(self, device_id):
        db = next(self.db())
        return db.query(DBDevice).filter(DBDevice.id == device_id).first()
