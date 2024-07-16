import uuid
from datetime import datetime, timedelta

from sqlalchemy import Boolean, Column, String, ForeignKey, Integer, UUID, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from ..models import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(EmailType, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    password_reset_token = relationship("PasswordResetToken", back_populates="user")


# Token sent to user email when resetting password
class PasswordResetToken(AbstractBaseModel):
    __tablename__ = "password_reset_tokens"
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates='password_reset_token')
    token = Column(UUID, unique=True, index=True, default=str(uuid.uuid4()))
    expires_on = Column(DateTime,  default=datetime.utcnow() + timedelta(minutes=5))
