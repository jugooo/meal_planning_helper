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
app.config.update(SECRET_KEY=os.urandom(24))
db.init_app(app)

class Recipe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=False,nullable=False)
    recipe_name = db.Column(db.String(80),unique=False,nullable=False)
    recipe_ingredients = db.Column(db.String(250),unique=False,nullable=False)
    recipe_instructions = db.Column(db.String(250),unique=False,nullable=False)

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

@app.route('/login',methods=['GET','POST'])
def login():
    return flask.render_template('login.html')

@app.route('/handle_login',methods=['POST'])
def handle_login():
    return flask.redirect(flask.url_for('index_page'))
    # return flask.render_template('index.html')

# ------ Login Required Section ------ #

@app.route('/index')
def index_page():
    '''
    Display Homepage
    Categories
    After Category is selected display random recipe
    '''
    return flask.render_template('index.html')

#Returns a list of saved recipes
@app.route('/saved_recipes',methods=['GET','POST'])
def saved_recipes():
    return flask.render_template('saved_recipes.html')

# @app.route('/pull_saved_recipes')
#Call inside of saved recipes to get query
def view_saved_recipes(username):
    saved_recipes = Recipe.query.filter_by(username=username).all()
    return saved_recipes

@app.route('/handle_save_recipe', methods=['GET','POST'])
def handle_save_recipe():
    recipe_form = flask.request.form
    recipe_user = recipe_form['username_field']
    recipe_name = recipe_form['name']
    recipe_ingredients = recipe_form['ingredients']
    recipe_instructions = recipe_form['instructions']
    saved_rec = Recipe(username=recipe_user,recipe_name=recipe_name,recipe_ingredients=recipe_ingredients,recipe_instructions=recipe_instructions)
    db.session.add(saved_rec)
    db.session.commit()
    flask.flash("Recipe has been saved")
    return flask.redirect(flask.url_for('index_page'))



if __name__ == "__main__":
    app.run(debug=True)