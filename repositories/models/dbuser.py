import uuid
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID

from repositories.base_repository import Base


class DBUser(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, nullable=False,)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class DBDevice(Base):
    __tablename__ = 'devices'
    id = Column(String, primary_key=True, nullable=False)
    digital_twin = Column(String, nullable=True)
    user_email = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
