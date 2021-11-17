import enum
from db_connect import db
from datetime import datetime


class User(db.Model):
    __tablename__="user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(200), nullable=False)
    # reservation_num=db.Column(db.Integer, default=0, nullable=False)
    # rented_num=db.Column(db.Integer, default=0, nullable=False)

    def __init__ (self, user_id, password):
        self.user_id=user_id
        self.password=password
    
class Book (db.Model):
    __tablename__='book'

    id=db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title=db.Column(db.String(100), nullable=False)
    publisher=db.Column(db.String(100), nullable=False)
    author=db.Column(db.String(100), nullable=False)
    publication_date=db.Column(db.DateTime, nullable=False)
    pages=db.Column(db.Integer, nullable=False)
    isbn=db.Column(db.String(15), nullable=False)
    description=db.Column(db.Text(), nullable=False)
    link=db.Column(db.String(200), nullable=False)
    img_url=db.Column(db.String(200), nullable=False)

class Comment (db.Model):
    __tablename__='comment'

    id = db.Column(db.Integer, primary_key=True,              nullable=False, autoincrement=True)

    author_id = db.Column(db.String(100), nullable=False)
    #foreign key 임 referencing user_id

    content = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating= db.Column(db.Integer, nullable=False)

class Rented (db.Model):
    __tablename__='rented'
    id = db.Column(db.Integer, primary_key=True,              nullable=False, autoincrement=True)
    title=db.Column(db.String(100), nullable=False)


