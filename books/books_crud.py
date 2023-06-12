from sqlalchemy.orm import Session

from books import books_service
from models import Book, Scrap


def find_one(db: Session, isbn: str):
    return db.query(Book).filter_by(isbn=isbn).one_or_none()


def create_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def find_one_or_create_if_none(db: Session, isbn: str):
    """
    db에서 book 조회후
    - 존재하면 리턴.
    - 존재하지 않으면 naver api에서 조회후, book row 생성후 반환
    :param db:
    :param isbn:
    :return:
    """
    book = find_one(db, isbn)
    if book is None:
        book = books_service.get_book(isbn)
        book = create_book(db, book)
    return book


def get_scraps_by_book(db: Session, isbn: str):
    return db.query(Scrap).filter_by(book_isbn=isbn).all()