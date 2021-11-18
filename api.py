from flask import url_for, redirect, request, render_template, jsonify, Blueprint, session, g
from models import *
from db_connect import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
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
            id=request.form["email"]
            name=request.form["name"]
            pw=request.form["password"]
            pw2 = request.form["password2"]

            #암호화 시킨후 저장
            user_data = User.query.filter(User.user_id == id).first()

            if user_data is not None:
                return '이미 가입하셨습니다'

            db.session.add(User(id,pw,name))
            db.session.commit()
            return '회원가입 성공'

        else:
            id = request.form["email"]
            pw = request.form["password"]

            user_data = User.query.filter(User.user_id==id).first()
            if not user_data:
                return '없는 아이디 입니다'
            elif pw!= user_data.password:
                return '비밀번호가 틀렸습니다'
            else:
                session.clear()
                session['user_id']=id
                session['name']=user_data.user_name
                
                return render_template('login.html')

@board.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('board.home'))




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

