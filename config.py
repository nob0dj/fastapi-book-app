import os

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    base_dir = os.path.abspath(os.path.dirname(__file__))  # 프로젝트 루트디렉토리
    # basdir 경로안에 DB파일 만들기
    db_file = os.path.join(base_dir, 'db.sqlite')
    # SQLAlchemy 설정
    # DB URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file
    # 비지니스 로직이 끝날때 Commit 실행(DB반영)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 수정사항에 대한 TRACK
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_SECRET_KEY
    JWT_SECRET_KEY = 'fastapi-book-app-secret'
    # JWT 알고리즘
    JWT_ALGORITHM = 'HS256'


configs = AppConfig()
