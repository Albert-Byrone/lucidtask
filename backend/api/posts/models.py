from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from backend.api.models import AbstractBaseModel



class Post(AbstractBaseModel):
    __tablename__ = 'posts'

    text = Column(String)


