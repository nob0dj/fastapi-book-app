from datetime import datetime
from pydantic import BaseModel

from auth.auth_schemas import UserRef
from books.books_schemas import BookRef


class ScrapBase(BaseModel):
    book_isbn: str
    content: str

    class Config:
        """
        model은 schema로 자동매핑되지 않는다.
        이후 router의 response_model에 해당 schema작성시 return객체의 유효성을 자동매핑해 처리할 수 있다
        """
        orm_mode = True


class Scrap(ScrapBase):
    """
    response용 Lang schema
    """
    id: int
    created_at: datetime
    user: UserRef
    book: BookRef


class ScrapCreate(ScrapBase):
    pass


class ScrapUpdate(BaseModel):
    content: str
