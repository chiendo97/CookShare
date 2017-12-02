# import library
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# MySql configurations
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '27091997'
app.config['MYSQL_DATABASE_DB'] = 'CookShare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#engine = create_engine('sqlite:///')
#base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def welcome():
    return render_template(
            'index.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    #Create user code
    # Read the posted value from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _name and _email and _password:

        conn = mysql.connect()
        cursor = conn.cursor()

        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sp_createUser',(_name,_email,_password))
        # return json.dumps({'html': '<spam>Debug</spam>'})
        data = cursor.fetchall()
        # return json.dumps({'html': '<spam>Debug</spam>'})
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error:': str(data[0])})
    else:
        return json.dumps({'html':'<spam>Enter the required fileds</spam>'})

#@app.route('/login')
#def login():
    #return "This site for login"

# @app.route('/register')
# def register():
#     return "This site for register"

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
    app.run(port=5002)
    # app.run(host='0.0.0.0', port=1234)
