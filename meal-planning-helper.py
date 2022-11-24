import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_user,current_user,login_required

#Load Env Vars
DATABASE_URL = os.getenv('DATABASE_URL')

#Create Extension
db = SQLAlchemy()

#Initize App
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL #Configure SQL Alchemy Database URL
db.init_app(app)

class Recipe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    recipe_name = db.Column(db.String(80),unique=False,nullable=False)
    recipe_ingredients = db.Column(db.String(250),unique=False,nullable=False)
    recipe_instructions = db.Column(db.String(250),unique=False,nullable=False)
    recipe_category = db.Column(db.String(80),unique=False,nullable=False)

    def __repr__(self) -> str:
        return '<Recipe%r>' % self.id
    
#Create Columns in Database
with app.app_context():
    db.create_all()



@app.route('/',methods=['GET'])
def inital_menu():
    return flask.render_template('inital_menu.html')

@app.route('/register', methods=['GET','POST'])
def create_account():
    return flask.render_template('register.html')

@app.route('/login')
def login():
    return flask.render_template('login.html')


# ------ Login Required Section ------ #



if __name__ == "__main__":
    app.run(debug=True)