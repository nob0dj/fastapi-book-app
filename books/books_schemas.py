from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    isbn: str

    class Config:
        orm_mode = True


class Book(BookBase):
    title: str
    link: str
    image: str
    author: str
    discount: str
    publisher: str
    pubdate: str
    description: str
    # scraps: List[Optional[Scrap]]  # 순환 참조 해결을 위한 ForwardRef Not working!
    # kollections: List[Optional['Kollection']] # pydantic.errors.ConfigError: field "kollections" not yet prepared so type is still a ForwardRef, you might need to call Book.update_forward_refs().


class BookRef(BookBase):
    title: str
    author: str
    publisher: str
