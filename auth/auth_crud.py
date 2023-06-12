from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from flask import abort
from sqlalchemy.orm import Session

from auth import auth_schemas
from config import configs

from models import User


def create_user(db: Session, data: auth_schemas.UserCreate) -> User:
    raw_password = data.password;
    encrypted_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=data.username, password=encrypted_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(user)
    return user


# def signin(db: Session, data: auth_schemas.UserSignin):
def signin(db: Session, form_data: OAuth2PasswordRequestForm):
    username = form_data.username
    password = form_data.password

    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=400, detail=f'{username} Not Found!')

    password_matched = bcrypt.checkpw(password.encode('utf-8'), user.password)
    if not password_matched:
        raise HTTPException(status_code=400, detail=f'Password Not Matched!')

    payload = {
        'id': user.id,
        'username': user.username,
        'grade': user.grade.name
    }
    return {
        'access_token': generate_access_token(payload),
        'refresh_token': generate_refresh_token(payload),
        'token_type': 'bearer'
    }


def generate_access_token(payload):
    payload.update(exp=datetime.utcnow() + timedelta(minutes=30))
    return jwt.encode(payload, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)


def generate_refresh_token(payload):
    payload.update(exp=datetime.utcnow() + timedelta(hours=2))
    return jwt.encode(payload, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)


def find_by_username(db: Session, username: str):
    return db.query(User).filter_by(username=username).one()