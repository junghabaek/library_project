import pymysql
from flask import Flask
from api import board
from db_connect import db


app= Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:614614@218.156.161.205:5000/library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)
if __name__ =='__main__':
    app.run('0.0.0.0', 5000, debug=True )