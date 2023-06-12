from sqlalchemy.orm import Session

from books import books_crud, books_service
from models import Scrap, Book, User
from scraps import scraps_schemas


def read_scraps(db: Session, username: str = None):
    if username is None:
        return db.query(Scrap).order_by(Scrap.id.desc()).all()
    user_id = db.query(User).filter_by(username=username).one().id
    return db.query(Scrap).filter_by(user_id=user_id).order_by(Scrap.id.desc()).all()


def read_scrap(db: Session, id: int):
    return db.query(Scrap).filter_by(id=id).first()


def create_scrap(db: Session, data: scraps_schemas.ScrapCreate, user: User):
    book = books_crud.find_one(db, data.book_isbn)
    if book is None:
        book = Book(books_service.get_book(data.book_isbn))
        books_crud.create_book(db, book)

    scrap = Scrap(book_isbn=data.book_isbn, content=data.content)
    scrap.user_id = user.id
    db.add(scrap)
    db.commit()
    db.refresh(scrap)  # db로부터 갱신된 정보 가져오기
    return scrap


def update_scrap(db: Session, scrap: Scrap, data: scraps_schemas.ScrapUpdate):
    scrap.content = data.content
    db.commit()
    return scrap


def delete_scrap(db: Session, scrap: Scrap):
    db.delete(scrap)
    db.commit()
