from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from books import books_schemas, books_service, books_crud
from database import get_db
from scraps.scraps_schemas import Scrap

router = APIRouter(prefix='/books')


# Session객체 의존주입은 router handler안에서만 작동한다.
@router.get('/search', response_model=list[books_schemas.Book], description='네이버 책검색 API - 검색')
def search_books(query: str, db: Session = Depends(get_db)):
    return books_service.search_books(query)


@router.get('/{isbn}', response_model=books_schemas.Book)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = books_crud.find_one(db, isbn)
    if book:
        return book
    return books_service.get_book(isbn)


@router.get('/{isbn}/scraps', response_model=List[Optional[Scrap]])
def get_scraps_by_book(isbn: str, db: Session = Depends(get_db)):
    return books_crud.get_scraps_by_book(db, isbn)
