from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette import status

from auth import auth_schemas, auth_crud, auth_validation
from auth.auth_validation import JWTBearer
from database import get_db
from models import User
from scraps import scraps_crud
from scraps.scraps_schemas import Scrap

router = APIRouter(prefix='/auth')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


@router.post('/signup', response_model=auth_schemas.User)
def signup(data: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    user = auth_crud.create_user(db, data)
    return user


# @router.post('/signin', response_model=auth_schemas.Token)
# @router.post('/signin', response_model=Dict[str, str])
# def signin(data: auth_schemas.UserSignin, db: Session = Depends(get_db)):
#     """로그인 성공시 AccessToken/RefreshToken 발행"""
#     return auth_crud.signin(db, data)

@router.post('/signin', response_model=Dict[str, str])
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data)  # <fastapi.security.oauth2.OAuth2PasswordRequestForm object at 0x112c6f150>
    return auth_crud.signin(db, form_data)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJob25nZ2QiLCJncmFkZSI6IkJBU0lDIiwiZXhwIjoxNjg1ODY1MTA5fQ.dxqUaVjRCFQwNXctkzoaBb-7pihnzbELSQ_m6e9e0ms",
        "username": "honggd"
    }
    """
    try:
        payload = auth_validation.decode_jwt(token)
        username = payload.get('username')
        return auth_crud.find_by_username(db, username)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token Expired! Please Login!'
        )
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}, # 옵션
        )



@router.get('/{username}')
def find_by_username(username: str, user: User = Depends(get_current_user)):
    # return {'token': token, 'username': username}
    # return auth_crud.find_by_username(db, username)
    print(user) # __repr__을 통해 scraps 정보를 다시 조회하게 된다.
    return user


# @router.get('/{username}', dependencies=[Depends(JWTBearer())], response_model=auth_schemas.User)
def find_by_username(username: str, db: Session = Depends(get_db)) -> User:
    """
    jwt 인증성공시에만 회원정보조회
    :param username:
    :param db:
    :return:
    """
    return auth_crud.find_by_username(db, username)

@router.get('/{username}/scraps')
def find_scraps_by_username(username: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> List[Optional[Scrap]]:
    print(user)
    return scraps_crud.read_scraps(db, user.username)
