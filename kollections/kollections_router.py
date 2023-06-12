from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from auth.auth_router import get_current_user
from database import get_db
from kollections import kollections_schema, kollections_crud
from models import User, Kollection

router = APIRouter(prefix='/kollections')


@router.post('', response_model=kollections_schema.Kollection)
def create_kollection(data: kollections_schema.KollectionCreate, user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return kollections_crud.create_kollection(db, data, user)


@router.get('/{id}', response_model=kollections_schema.Kollection)
def get_kollection(id: int, db: Session = Depends(get_db)):
    return kollections_crud.get_kollection(db, id)


@router.delete('/{id}')
def delete_kollection(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    kollections_crud.delete_kollection(db, id, user)
    return Response(status_code=204)  # fastapi.Response = starlette.reponses


@router.patch('/{id}', response_model=kollections_schema.Kollection)
def update_kollection(id: int, data: kollections_schema.KollectionUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return kollections_crud.update_kollection(db, id, data, user)


@router.post('/{id}/books', response_model=kollections_schema.Kollection)
def add_books_to_kollection(id: int, data: kollections_schema.KollectionAddBooks, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return kollections_crud.add_books_to_kollection(db, id, data, user)


@router.delete('/{id}/books/{book_isbn}', response_model=kollections_schema.Kollection)
def remove_from_kollection(id: int, book_isbn: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return kollections_crud.remove_from_kollection(db, id, book_isbn, user)

