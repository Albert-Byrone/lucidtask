
from fastapi_camelcase import CamelModel
from .schemas import GetPost
from backend.api.utils import ResponseModel
from typing import List


class CreatePostData(CamelModel):
    post: GetPost | None


class CreatePostResponse(ResponseModel):
    data: CreatePostData = CreatePostData()


class GetPostsData(CamelModel):
    posts: List[GetPost] | None


class GetPostResponse(ResponseModel):
    data: GetPostsData = GetPostsData()

