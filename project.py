# import library
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#engine = create_engine('sqlite:///')
#base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/')
@app.route('/index')
def welcome():
    return render_template(
            'index.html')

#@app.route('/login')
#def login():
    #return "This site for login"

@app.route('/register')
def register():
    return "This site for register"

@app.route('/user/<int:user_id>')
def user(user_id):
    return "This site for showing user"

@app.route('/<int:food_id>')
def food(food_id):
    return "This site for showing food"

@app.route('/<int:food_id>/edit')
def editFood(food_id):
    return "This site for editing food"

@app.route('/create')
def createFood():
    return "This site for creating food"

@app.route('/<int:food_id>/commend')
def commendFood(food_id):
    return "This site for commending food"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=1234)
