import pymysql
from flask import Flask
from api import board
from db_connect import db
from flask_migrate import Migrate

app= Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:614614@127.0.0.1:3306/library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = "614614"
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)

Migrate().init_app(app, db)




if __name__ =='__main__':
    app.run('0.0.0.0', 5000, debug=True )
