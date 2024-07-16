from __future__ import absolute_import, unicode_literals

import os
import base64
import datetime
import json
import uuid

import requests
from requests.auth import HTTPBasicAuth
from fastapi import WebSocketException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from ..configs.database_config import SessionLocal
from dotenv import load_dotenv

load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResponseModel(BaseModel):
    success: bool = False
    data: dict | None
    message: str | None

class Config:
    orm_mode = True

def get_token():
    return OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_token_ws(
        jwt_token: str | None,
):
    if jwt_token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return jwt_token