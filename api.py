from flask import redirect, request, render_template, jsonify, Blueprint, session, g
#from models import User, Post
from db_connect import db
#from flask_bcrypt import Bcrypt

board = Blueprint('board', __name__)
#bcrypt = Bcrypt()

@board.route("/")
def home():
    return render_template('index.html')

# @board.route('/signup')
# def signup():
