from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from auth.auth_schemas import UserRef
from books.books_schemas import Book


class KollectionBase(BaseModel):
    class Config:
        """
        model은 schema로 자동매핑되지 않는다.
        이후 router의 response_model에 해당 schema작성시 return객체의 유효성을 자동매핑해 처리할 수 있다
        """
        orm_mode = True

class Kollection(KollectionBase):
    id: int
    name: str
    user_id: int
    user: UserRef
    created_at: datetime
    modified_at: Optional[datetime]
    books: List[Optional[Book]]


class KollectionCreate(BaseModel):
    name: str


class KollectionUpdate(KollectionCreate):
    pass


class KollectionAddBooks(BaseModel):
    books: List[str] # book_isbn