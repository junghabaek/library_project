from flask import url_for, redirect, request, render_template, jsonify, Blueprint, session, g, flash
from datetime import datetime
from flask.helpers import get_flashed_messages
from models import *
from db_connect import db
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()
board = Blueprint('board', __name__)

#url_prefix='/'

@board.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@board.route("/login", methods=['POST', 'GET'])
def login():
    if request.method=="GET":
        #return render_template('index.html')
        return redirect(url_for('board.home'))
    elif request.method=="POST":
        if request.form["password2"]:
            id=request.form["email2"]
            name=request.form["name"]
            pw1=request.form["password1"]
            pw2 = request.form["password2"]
            
            if pw1!=pw2:
                flash('비밀번호가 일치하지 않습니다.')

                return redirect(url_for('board.home'))
            else:
                pw_hash=generate_password_hash(pw1)
                user_data = User.query.filter(User.user_id == id).first()

                if user_data is not None:
                    flash('이미 가입된 이메일입니다.')
                    return redirect(url_for('board.home'))
                else:
                    db.session.add(User(id,pw_hash,name))
                    db.session.commit()
                    flash('환영합니다! 로그인 해 주세요.')
                    return redirect(url_for('board.home'))#flash
# flash()
# {% for message in get_flashed_messages() %}
# <div class='alert alert-info'>
#     {{message}}
# </div>
# {% endfor %}
        #로그인 구현
        else:
            id = request.form["email"]
            pw = request.form["password"]
            
            user_data = User.query.filter(User.user_id==id).first()
            if not user_data:
                flash('없는 아이디 입니다. 가입을 해 주세요')
                return redirect(url_for('board.home'))
            elif not check_password_hash(user_data.password, pw):
                flash('비밀번호를 다시 확인해 주세요.')
                return redirect(url_for('board.home'))
            else:
                session.clear()
                session['user_id']=id
                session['name']=user_data.user_name
                flash('환영합니다!')
                return redirect(url_for('board.mainpage'))

@board.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('board.home'))

@board.route('/mainpage', methods=['GET','POST'])
def mainpage():
    #책 이미지
    #책 제목
    #books_title_asc=
    books=Book.query.order_by(Book.title.asc())
    #img = "../static/img/9.png"

    return render_template('mainpage.html', cards=books)

@board.route('/mypage', methods=['GET','POST'])
def mypage():
    return render_template('mypage.html')


@board.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):

    if request.method == 'GET':
        book=Book.query.filter(Book.id==id).first()
        comment_list = Comment.query.filter(Comment.book_id == id).order_by(Comment.time.desc()).all()
        avg=Comment.query.filter(Comment.book_id==id).all()
        cnt=0
        sum=0
        for i in avg:
            sum+=i.rating
            cnt+=1
        if cnt==0:
            average=0
        else:
            average= round(sum/cnt,1)



        return render_template('details.html', card=book, comment_list=comment_list, average=average)
    else:
        comment = request.form['comment']
        rating=request.form['rating']
        book = Book.query.filter(Book.id == id).first()
        uid = User.query.filter(User.user_id == session['user_id']).first()
        com = Comment(uid.id, id, comment, rating, datetime.utcnow())
        db.session.add(com)
        db.session.commit()
        comment_list = Comment.query.filter(
            Comment.book_id == id).order_by(Comment.time.desc()).all()
        avg = Comment.query.filter(Comment.book_id == id).all()
        cnt = 0
        sum = 0
        for i in avg:
            sum += i.rating
            cnt += 1
        if cnt == 0:
            average = 0
        else:
            average = round(sum/cnt, 1)
        flash('댓글이 작성되었습니다')
        
        return render_template('details.html', card=book, comment_list=comment_list, average=average)


# @board.route('/signup')
# def signup():

#store_list=rabbitStore.query.order_by(rabbitStore.name.asc())

# db.session.add(user)
# db.session.commit()

# {{ url_for('board.register')}}

# {% include "+navbar.html" %} 파일 갖다 붙히기


# {% extends "base.html" %}
# {% block page_content %}
# {% endblock %}

