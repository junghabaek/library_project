from flask import url_for, redirect, request, render_template, jsonify, Blueprint, session, g, flash
from datetime import datetime
from flask.helpers import get_flashed_messages
from models import *
from db_connect import db
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()
board = Blueprint('board', __name__)

# url_prefix='/'


@board.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@board.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        # return render_template('index.html')
        return redirect(url_for('board.home'))
    elif request.method == "POST":
        if request.form["password2"]:
            id = request.form["email2"]
            name = request.form["name"]
            pw1 = request.form["password1"]
            pw2 = request.form["password2"]

            if pw1 != pw2:
                flash('비밀번호가 일치하지 않습니다.')

                return redirect(url_for('board.home'))
            else:
                pw_hash = generate_password_hash(pw1)
                user_data = User.query.filter(User.user_id == id).first()

                if user_data is not None:
                    flash('이미 가입된 이메일입니다.')
                    return redirect(url_for('board.home'))
                else:
                    db.session.add(User(id, pw_hash, name))
                    db.session.commit()
                    flash('환영합니다! 로그인 해 주세요.')
                    return redirect(url_for('board.home'))  # flash
# flash()
# {% for message in get_flashed_messages() %}
# <div class='alert alert-info'>
#     {{message}}
# </div>
# {% endfor %}
        # 로그인 구현
        else:
            id = request.form["email"]
            pw = request.form["password"]

            user_data = User.query.filter(User.user_id == id).first()
            if not user_data:
                flash('없는 아이디 입니다. 가입을 해 주세요')
                return redirect(url_for('board.home'))
            elif not check_password_hash(user_data.password, pw):
                flash('비밀번호를 다시 확인해 주세요.')
                return redirect(url_for('board.home'))
            else:
                session.clear()
                session['user_id'] = id
                session['name'] = user_data.user_name
                flash('환영합니다!')
                return redirect(url_for('board.mainpage'))


@board.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    flash('정상적으로 로그아웃 되셨습니다.')
    return redirect(url_for('board.home'))


@board.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    # 책 이미지
    # 책 제목
    # books_title_asc=
    books = Book.query.order_by(Book.title.asc())
    #img = "../static/img/9.png"

    return render_template('mainpage.html', cards=books)


@board.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    uid = User.query.filter(User.user_id == session['user_id']).first()
    if request.method == 'GET':

        book = Book.query.filter(Book.id == id).first()
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

        return render_template('details.html', card=book, comment_list=comment_list, average=average, uid=uid.id)
    else:
        
        # borrow = request.form["borrow"]
        # reserve = request.form["reserve"]
        # button이 안눌렸으니까 request.form['button']이 없다
        if request.form.get('borrow') is not None:
            # stock 하나 줄이기 book_id를 받아와서 query 해서 book 찾고, 그 book의 stock을 바꾼다.
            book = Book.query.filter(Book.id == id).first()

            # 어떤 유저가 빌린 어떤 책인데, 반납하지 않은 책이 있으면 대여 안해줌.
            already_have = Rented.query.filter(Rented.book_id == id).filter(
                Rented.user_id == uid.id).filter(Rented.returned_time == None).first()

            if already_have is not None:
                flash('이미 대여중인 책입니다.')
                return redirect(url_for('board.details', id=id))

            borrowed_more_than_2 = Rented.query.filter(
                Rented.user_id == uid.id).filter(Rented.returned_time == None).all()
            if len(borrowed_more_than_2) == 2:
                flash('책은 한번에 두 권 까지만 빌릴 수 있어요.')
                return redirect(url_for('board.details', id=id))

            if book.stock == 0:
                flash('재고가 없습니다.')
                return redirect(url_for('board.details', id=id))
            else:
                book.stock -= 1
                # uid 받아와서, 대출에 레코드 추가

                rented_record = Rented(uid.id, id)
                db.session.add(rented_record)
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
                flash('행복한 시간 되세요~!')
                return render_template('details.html', card=book, comment_list=comment_list, average=average, uid=uid.id)

        elif request.form.get("reserve") is not None:

            # 한사람당 두 권 까지 예약 가능
            book = Book.query.filter(Book.id == id).first()
            # uid 받아와서, 예약에 레코드 추가, 단 한 사람은 세 권 까지만 예약을 할 수 있고, 한 책에는 네 명 이상 예약 불가능
            # 책이 아직 남아있을 때는 그냥 대여하기로 안내하기
            if book.stock != 0:
                flash('아직 재고가 남아있습니다. 대여를 해 보세요')
                return redirect(url_for('board.details', id=id))

            already_have = Rented.query.filter(Rented.book_id == id).filter(
                Rented.user_id == uid.id).filter(Rented.returned_time == None).first()

            if already_have is not None:

                flash('이미 대여중인 책엔 예약을 할 수 없어요.')
                return redirect(url_for('board.details', id=id))

            already_reserved = Reservation.query.filter(Reservation.book_id == id).filter(
                Reservation.user_id == uid.id).filter(Reservation.isReserved == True).first()

            if already_reserved is not None:
                flash('이미 예약을 걸어놓은 책입니다.')
                return redirect(url_for('board.details', id=id))

            already_have = Rented.query.filter(Rented.book_id == id).filter(
                Rented.user_id == uid.id).filter(Rented.returned_time == None).first()

            if already_have is not None:
                flash('이미 대여중인 책입니다.')
                return redirect(url_for('board.details', id=id))

            isReserverMoreThanThree = Reservation.query.filter(
                Reservation.book_id == id).filter(Reservation.isReserved == True).all()

            if len(isReserverMoreThanThree) == 3:
                flash('예약은 세 명 까지만 할 수 있어요.')
                return redirect(url_for('board.details', id=id))

            hasUserReservedMoreThanThree = Reservation.query.filter(
                Reservation.user_id == uid.id).filter(Reservation.isReserved == True).all()

            if len(hasUserReservedMoreThanThree) == 3:
                flash('예약은 세 권 까지만 할 수 있어요')
                return redirect(url_for('board.details', id=id))

            reservation = Reservation(uid.id, id)

            db.session.add(reservation)
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

            return render_template('details.html', card=book, comment_list=comment_list, average=average, uid=uid.id)

        

        elif request.form.get('comment') is not None:
            comment = request.form['comment']
            rating = request.form['rating']
            book = Book.query.filter(Book.id == id).first()

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

            return render_template('details.html', card=book, comment_list=comment_list, average=average, uid=uid.id)
        
        
        if request.form.get("update") is not None:
            comment_id = request.form['update']
            # comment의 id를 프론트에서 받아온다음 백에서 update하고, redirect
            comment = Comment.query.filter(Comment.id == comment_id).first()
            comment.content = request.form['updatecomment']
            db.session.commit()
            return redirect(url_for('board.details', id=id))

        if request.form.get("delete") is not None:
            comment_id = request.form['delete']
            comment = Comment.query.filter(Comment.id == comment_id).first()
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('board.details', id=id))




@board.route('/mypage', methods=['GET', 'POST'])
def mypage():
    uid = User.query.filter(User.user_id == session['user_id']).first()
    #borrowed_more_than_2 = Rented.query.filter(Rented.user_id == uid.id).filter(Rented.returned_time == None).all()

    if len(Rented.query.filter(Rented.user_id == uid.id).filter(Rented.returned_time == None).all()) > 2:
        flash("예약하신 책에 한에서는 한도가 넘어도 대여를 해 드리지만, 책을 3권 이상 빌렸으니 한권은 빨리 반납해 주세요.")
###책반납###

    if request.method == 'POST':
        # button2를 눌렀을 때 button이 안눌렸기에, request.form['button'] 자체가 없다

        returned_book_id = request.form['button']
        returned_book = Rented.query.filter(Rented.user_id == uid.id).filter(
            Rented.book_id == returned_book_id).filter(Rented.returned_time == None).first()

        if returned_book is not None:
            returned_book.returned_time = datetime.utcnow()
            updateStock = Book.query.filter(
                Book.id == returned_book_id).first()
            updateStock.stock += 1

            if updateStock.stock == 1:
                updateReservation = Reservation.query.filter(
                    Reservation.book_id == returned_book_id).filter(Reservation.isReserved == True).first()
                if updateReservation is not None:
                    updateUserId = updateReservation.user_id
                    updateReservation.isReserved = False  # 예약 끝 => 대여하기

                    # 만약 빌린 책이 두권 이상이면? 예약을 못하게 하거나
                    # 대여를 시켜주되 반납을 빨리 해달라는 메세지

                    newRent = Rented(updateUserId, returned_book_id)
                    db.session.add(newRent)
                    updateStock.stock = 0
                    db.session.commit()

                    return redirect(url_for('board.mypage'))

##################

# book = Book.query.filter(Book.id == id).first()
#          uid = User.query.filter(User.user_id == session['user_id']).first()
#           # 어떤 유저가 빌린 어떤 책인데, 반납하지 않은 책이 있으면 대여 안해줌.
#           already_have = Rented.query.filter(Rented.book_id == id).filter(
#                Rented.user_id == uid.id).filter(Rented.returned_time == None).first()

#            if already_have is not None:
#                 return '이미 대여중인 책입니다.'

#             borrowed_more_than_2 = Rented.query.filter(
#                 Rented.user_id == uid.id).filter(Rented.returned_time == None).all()
#             if len(borrowed_more_than_2) == 2:
#                 return '책은 한번에 두 권 까지만 빌릴 수 있어요.'

#             if book.stock == 0:
#                 return '재고가 없습니다.'
#             else:
#                 book.stock -= 1
#                 # uid 받아와서, 대출에 레코드 추가

#                 rented_record = Rented(uid.id, id)
#                 db.session.add(rented_record)
#                 db.session.commit()

#############

            # 만약 stock이 1이증가해서 stock이 1이 됐으면,
            # 예약자가 있는지 확인해 봅니다
            # 예약자가 있으면 그 예약

            db.session.commit()
            flash('책이 성공적으로 반납되었습니다.')
            return redirect(url_for('board.mypage'))

        cancellation_id = request.form['button']
        cancelled_book = Reservation.query.filter(Reservation.user_id == uid.id).filter(
            Reservation.book_id == cancellation_id).filter(Reservation.isReserved == True).first()

        if cancelled_book is not None:
            cancelled_book.isReserved = False
            db.session.commit()
            flash('도서 예약이 취소되었습니다.')
            return redirect(url_for('board.mypage'))

    else:

        # rented_books_for_query=Rented.query.filter(Rented.user_id==uid.id).filter(Rented.returned_time==None).all()
        book = Rented.query.filter(Rented.user_id == uid.id).filter(
            Rented.returned_time == None).all()  # 유저가 빌려간 책들의 레코드
        rented_books_list = []
        for i in book:
            book_title = Book.query.filter(Book.id == i.book_id).first()
            rented_books_list.append(book_title)

        reserved_book = Reservation.query.filter(
            Reservation.user_id == uid.id).filter(Reservation.isReserved == True).all()

        reserved = []
        for i in reserved_book:
            reserved_book_title = Book.query.filter(
                Book.id == i.book_id).first()
            reserved.append(reserved_book_title)

        #reserved_books_line= Reservation.query.filter(Reservation.user_id==uid).filter(Reservation.isReserved== True).all()
        # 내가 예약한 책들의 레코드 최대 3권-> 각각의 레코드의 book_id로 책을 예약한 레코드 검색 최대 3권
        # 각각의 레코드의 갯수를 화면에 반환... 어떻게?

        # numthree=len(Reservation.query.filter(Reservation.book_id==reserved_books_line).all())

        reserved_num = {}

        for i in reserved_book:  # reserved_book은 내가 빌린 책 최대 2권
            book = Reservation.query.filter(Reservation.book_id == i.book_id).filter(
                Reservation.isReserved == True).filter(Reservation.id < i.id).all()  # 다른 사람들의 예약 레코드 리스트
            reserved_num[i.book_id] = len(book)

        # book.id를 받아와야 하는데, reserved_book에서 book_id와 isReserved인 책을 검색한다.
        # reserved_users = Reservation.query.filter(
        #     Reservation.book_id == i.book_id).filter(Reservation.isReserved == True).all()

        book_returned = Rented.query.filter(Rented.user_id == uid.id).filter(
            Rented.returned_time != None).all()
        # 유저가 반납한 책들의 레코드
        # 반납한 책의 book_id를 가져와서 책의 이미지와 타이틀을 가져와야함
        # rented 레코드를 프론트로 보내야함
        rented_books_list_for_returned = []
        for i in book_returned:
            returned_returned = Book.query.filter(Book.id == i.book_id).first()
            rented_books_list_for_returned.append(returned_returned)

        rented_books_list_for_returned = list(
            set(rented_books_list_for_returned))
        numfo = len(book_returned)

        returned_list = Rented.query.filter(Rented.user_id == uid.id).filter(
            Rented.returned_time != None).order_by(Rented.id.asc()).all()

        # for i in book_returned:
        #     book_returned_bookid = Rented.query.filter(Rented.user_id == uid.id).filter(
        #         Rented.returned_time != None).filter(Rented.book_id == i.book_id).first()
        #     # 빌려간 책들중에 한 유저가 빌렸다가 반납한 certain 책의 레코드들을 list로 저장
        #     returned_list.append(book_returned_bookid)

        return render_template('mypage.html', cards=rented_books_list, reserved=reserved, num=len(rented_books_list), numtwo=len(reserved), numfo=numfo,
                               reserved_num=reserved_num, returned_list=returned_list, rented_books_list_for_returned=rented_books_list_for_returned)

# @board.route('/signup')
# def signup():

# store_list=rabbitStore.query.order_by(rabbitStore.name.asc())

# db.session.add(user)
# db.session.commit()

# {{ url_for('board.register')}}

# {% include "+navbar.html" %} 파일 갖다 붙히기


# {% extends "base.html" %}
# {% block page_content %}
# {% endblock %}
