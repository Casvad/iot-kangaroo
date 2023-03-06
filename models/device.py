from typing import Optional

from pydantic import BaseModel
import os


class Device(BaseModel):
    id: str = os.urandom(24).hex()
    mac: str
    digitalTwin: Optional[str]
