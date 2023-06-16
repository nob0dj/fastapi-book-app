import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = 'book'
    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    image = Column(String)
    author = Column(String)
    discount = Column(String)
    publisher = Column(String)
    pubdate = Column(String)
    description = Column(String)
    scraps = relationship("Scrap", back_populates='book')  # 단방향 참조라면 backref속성 사용
    kollections = relationship('Kollection', secondary='kollection_book', back_populates='books')

    def __init__(self, data):
        self.isbn = data['isbn']
        self.title = data['title']
        self.link = data['link']
        self.image = data['image']
        self.author = data['author']
        self.discount = data['discount']
        self.publisher = data['publisher']
        self.pubdate = data['pubdate']
        self.description = data['description']

    def __repr__(self):
        return f"Book(isbn={self.isbn}, title={self.title}, link={self.link}, image={self.image}, author={self.author}, discount={self.discount}, publisher={self.publisher}, pubdate={self.pubdate}, description={self.description})"


class Scrap(Base):
    __tablename__ = 'scrap'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String, ForeignKey('book.isbn'), nullable=False)  # 자식테이블에 fk설정(두번째 인자로 전달)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    book = relationship('Book', back_populates='scraps', lazy='joined')
    user_id = Column(String, ForeignKey('user.id'))
    user = relationship('User', back_populates='scraps', lazy='joined')  # select(기본값) joined subquery selectin noload

    def __init__(self, **data):
        self.id = data['id'] if 'id' in data else None
        self.book_isbn = data['book_isbn']
        self.content = data['content']
        self.created_at = data['created_at'] if 'creted_at' in data else None

    def __repr__(self):
        return f"Scrap(id={self.id!r}, book_isbn={self.book_isbn!r} content={self.content!r}, created_at={self.created_at!r}, user_id={self.user_id}, book={self.book})"


class UserGrade(enum.Enum):
    """
    name = value
    실제 db저장할때는 name값이 저장된다.
    """
    BASIC = 'basic'
    PREMIUM = 'premium'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    grade = Column(Enum(UserGrade), default=UserGrade.BASIC)
    created_at = Column(DateTime, default=datetime.now())
    scraps = relationship('Scrap', back_populates='user')
    kollections = relationship('Kollection', back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.grade = UserGrade.BASIC

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, password={self.password}, grade={self.grade}, created_at={self.created_at}, scraps={self.scraps}, kollections={self.kollections})'


kollection_book = Table(
    'kollection_book',
    Base.metadata,
    Column('kollection_id', Integer, ForeignKey('kollection.id')),
    Column('book_isbn', Integer, ForeignKey('book.isbn'))
)


class Kollection(Base):
    __tablename__ = 'kollection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='kollections')
    books = relationship('Book', secondary='kollection_book', back_populates='kollections')
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime)

    def __init__(self, name, user):
        self.name = name
        self.user = user

    def __repr__(self):
        return f'Kollection(id={self.id}, name={self.name}, user_id={self.user_id}, books={self.books})'
