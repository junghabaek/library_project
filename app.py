from flask import Flask
from api import board
from db_connect import db


app= Flask(__name__)
app.register_blueprint(board)


db.init_app(app)
if __name__ =='__main__':
    app.run('0.0.0.0', 5000, debug=True )