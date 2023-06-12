from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from books import books_crud
from kollections import kollections_schema
from models import User, Kollection


def create_kollection(db: Session, data: kollections_schema.KollectionCreate, user: User):
    kollection = Kollection(name=data.name, user=user)
    db.add(kollection)
    db.commit()
    db.refresh((kollection))
    return kollection



def get_kollection(db: Session, id: int):
    try:
        kollection = db.query(Kollection).filter_by(id=id).one()
        return kollection
    except NoResultFound:
        raise HTTPException(status_code=404, detail='No kollection found!')


def delete_kollection(db: Session, id: int, user: User):
    kollection = get_kollection(db, id)
    if kollection.user_id != user.id:
        raise HTTPException(status_code=400, detail='Has no permission!')
    db.delete(kollection)
    db.commit()


def update_kollection(db: Session, id: int, data: kollections_schema.KollectionUpdate, user: User):
    kollection: Kollection = get_kollection(db, id)
    if kollection.user_id != user.id:
        raise HTTPException(status_code=400, detail='Has no permission!')
    kollection.name = data.name
    db.commit()
    return kollection


def add_book_to_kollection(db: Session, kollection: Kollection, book_isbn: str):
    print(kollection.books)
    book = books_crud.find_one_or_create_if_none(db, book_isbn)
    kollection.books.append(book)



def add_books_to_kollection(db: Session, id: int, data: kollections_schema.KollectionAddBooks, user: User):
    kollection: Kollection = get_kollection(db, id)
    if kollection.user_id != user.id:
        raise HTTPException(status_code=400, detail='Has no permission!')
    for book_isbn in data.books:
        print(book_isbn)
        add_book_to_kollection(db, kollection, book_isbn)
    db.commit()
    db.refresh(kollection)
    return kollection


def remove_from_kollection(db: Session, id: int, book_isbn: str, user: User):
    kollection: Kollection = get_kollection(db, id)
    if kollection.user_id != user.id:
        raise HTTPException(status_code=400, detail='Has no permission!')
    books: [] = kollection.books
    found = False
    for book in books:
        print(book.isbn, book_isbn, type(book.isbn), type(book_isbn))
        if book.isbn == book_isbn:
            found = True
            books.remove(book)

    if not found:
        raise HTTPException(status_code=404, detail=f'Kollection has no book : {book_isbn}')

    return kollection