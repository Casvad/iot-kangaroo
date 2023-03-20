from pydantic import BaseModel


class DeviceTransaction(BaseModel):
    address: str
    signature: str
    data: str
