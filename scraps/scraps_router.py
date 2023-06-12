from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response, RedirectResponse

from auth.auth_router import get_current_user
from database import get_db
from models import User
from scraps import scraps_schemas
from scraps.scraps_crud import read_scraps, create_scrap, read_scrap, update_scrap, delete_scrap

router = APIRouter(prefix='/scraps')


# Session객체 의존주입은 router handler안에서만 작동한다.
@router.get('', response_model=list[scraps_schemas.Scrap])
def scraps(db: Session = Depends(get_db)):
    return read_scraps(db)


@router.post('', response_model=scraps_schemas.Scrap)
def scraps(data: scraps_schemas.ScrapCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    인증된 사용자만 scrap 등록. 사용자 정보는 jwt로 부터 가져온다.
    :param data:
    :param user:
    :param db:
    :return:
    """
    print(user)
    scrap = create_scrap(db, data, user)
    return Response(status_code=201, headers={'location': f'/scraps/{scrap.id}'})


# 기본값이 지정된 매개변수가 항상 뒤에 위치해야 한다.
@router.get('/{id}', response_model=scraps_schemas.Scrap)
def scraps(id: int, db: Session = Depends(get_db)):
    scrap = read_scrap(db, id)
    if scrap is None:
        raise HTTPException(status_code=404, detail="Scrap not found")
    return scrap


@router.patch('/{id}', response_model=scraps_schemas.Scrap)
def scraps(id: int, data: scraps_schemas.ScrapUpdate, db: Session = Depends(get_db)):
    scrap = read_scrap(db, id)
    if scrap is None:
        raise HTTPException(status_code=404, detail="Scrap not found")
    scrap = update_scrap(db, scrap, data)
    return scrap


@router.delete('/{id}')
def scraps(id: int, db: Session = Depends(get_db)):
    scrap = read_scrap(db, id)
    if scrap is None:
        raise HTTPException(status_code=404, detail="Scrap not found")
    delete_scrap(db, scrap)
    return Response(status_code=204)


@router.get('/users/{username}')
def scraps_by_user(username: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # print(username, user)
    return RedirectResponse(url=f"/auth/{username}/scraps")  # headers=headers 이전 요청 헤더 동일하게 요청
