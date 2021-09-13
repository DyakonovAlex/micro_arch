import uuid

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import PasswordType
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=256), nullable=False, unique=True)
    email = Column(String(length=128), nullable=False, unique=True)
    password = Column(
        PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'],
                     deprecated=['md5_crypt']),
        unique=False,
        nullable=False,
    )

    def __repr__(self):
        return f'Profile(id={self.id!r}, username={self.name!r})'


class Session(Base):
    __tablename__ = 'session'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payload = Column(JSON(), nullable=False)
