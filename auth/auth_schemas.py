from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from models import UserGrade


class UserBase(BaseModel):
    class Config:
        """
        model은 schema로 자동매핑되지 않는다.
        이후 router의 response_model에 해당 schema작성시 return객체의 유효성을 자동매핑해 처리할 수 있다
        """
        orm_mode = True


class User(UserBase):
    id: int
    username: str
    password: str
    grade: UserGrade
    created_at: datetime
    scraps: List[Optional['Scrap']]
    kollections: List[Optional['Kollection']]


class UserRef(UserBase):
    """
    Scrap에서 참조시 사용하는 UserSchema
    """
    id: int
    username: str
    grade: UserGrade

class UserSignin(UserBase):
    username: str
    password: str


class UserCreate(UserBase):
    username: str
    password: str


class Token(BaseModel):
    AccessToken: str
    RefreshToken: str

    class Config:
        orm_mode = True
