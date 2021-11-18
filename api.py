from flask import redirect, request, render_template, jsonify, Blueprint, session, g
#from models import User, Post
from db_connect import db
#from flask_bcrypt import Bcrypt

board = Blueprint('board', __name__)
#bcrypt = Bcrypt()
#url_prefix='/'

@board.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@board.route("/login", methods=['POST', 'GET'])
def login():
    id=request.form["email"]
    pw=request.form["password"]
    pw2 = request.form["password2"]
    return render_template('login.html',id=id, pw=pw, pw2=pw2)

# @board.route('/signup')
# def signup():
