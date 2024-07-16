from fastapi_camelcase import CamelModel
from datetime import datetime


class PostBase(CamelModel):
    text: str

class CreatePost(PostBase):
    pass


class GetPost(PostBase):
    id: int

    class Config:
        orm_mode = True

class UpdatePost(CamelModel):
    text: str


class PostRead(CamelModel):
    text: str
    created_at: datetime

    class Config:
        orm_mode = True