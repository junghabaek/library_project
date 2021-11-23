import enum
from db_connect import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, password, user_name):
        self.user_id = user_id
        self.password = password
        self.user_name = user_name


class Book (db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)
    stock = db.Column(db.Integer, nullable=True)


class Comment (db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # foreign key 임 referencing user_id
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    content = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, book_id, content, rating, time):
        self.user_id = user_id
        self.book_id = book_id
        self.content = content
        self.rating = rating
        self.time = time

class Rented (db.Model):
    __tablename__ = 'rented'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    #isReturned=db.Column(db.Boolean, default=False)
    rented_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    returned_time = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        
        
        


class Reservation (db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    isReserved = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

        #두잇 리액트 예약을 취소하면
        #앞에 1명이 대기하는것으로 바꿔야함
        #북아이디는 7번
        #유저 12번 아이디로 취소해보자
