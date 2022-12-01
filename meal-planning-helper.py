import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
from dotenv import load_dotenv
import os
import static.custom_classes as cc
from flask_login import LoginManager, login_user,current_user,login_required

#Load Env Vars
DATABASE_URL = os.getenv('DATABASE_URL')
# FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
API_KEY = os.getenv('API_KEY')

#Create Extension
db = SQLAlchemy()

#Initize App
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL #Configure SQL Alchemy Database URL
# app.config['SECRET KEY'] = FLASK_SECRET_KEY
app.config.update(SECRET_KEY=os.urandom(24))
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Recipe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=False,nullable=False)
    recipe_name = db.Column(db.String(150),unique=False,nullable=False)
    recipe_ingredients = db.Column(db.String(1000),unique=False,nullable=False)
    recipe_instructions = db.Column(db.String(1000),unique=False,nullable=False)

    def __repr__(self) -> str:
        return '<Recipe%r>' % self.id



class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)

    #Return the Person + username
    def __repr__(self) -> str:
        return '<Person%r>' % self.username

#Create Columns in Database
with app.app_context():
    db.create_all()


@app.route('/',methods=['GET'])
def inital_menu():
    return flask.render_template('inital_menu.html')

@app.route('/register', methods=['GET','POST'])
def create_account():
    return flask.render_template('register.html')

@app.route('/handle_register',methods=['GET','POST'])
def handle_register():
    #Get Form from register.html
    user_input = flask.request.form
    #id_input = user_input['id_input']
    username_input = user_input['username_input']

    create_user = Person(username = username_input)
    print('Created user', create_user)
    if not register_validate_username(username_input):
        #User already exists
        flask.flash("Username already exists")
        return flask.redirect(flask.url_for('login'))
    else:
        #adding user to DB
        db.session.add(create_user)
        db.session.commit()
        return flask.redirect(flask.url_for('index_page'))


    # return flask.redirect(flask.url_for('index_page'))

def register_validate_username(username_input):
    existing_user_username = Person.query.filter_by(username=username_input).first()
    if existing_user_username:
        return False
    return True

@app.route('/login',methods=['GET','POST'])
def login():
    return flask.render_template('login.html')

@app.route('/handle_login',methods=['POST'])
def handle_login():
    #Get form from login.html
    user_input = flask.request.form
    username_input = user_input['username_input']
    existing_user = Person.query.filter_by(username=username_input).first()
    if existing_user:
        login_user(existing_user)
        return flask.redirect(flask.url_for('index_page'))
    else:
        flask.flash('Incorrect Credentials')
        return flask.redirect(flask.url_for('login'))

    # return flask.redirect(flask.url_for('index'))
    # # return flask.render_template('index.html')



# ------ Login Required Section ------ #
@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(user_id)

@login_required
@app.route('/index')
def index_page():
    '''
    Display Homepage
    Categories
    After Category is selected display random recipe
    '''
    recipe_dict = cc.pull_api_data(API_KEY)
    return flask.render_template(
        'index.html',
         recipe_name=recipe_dict['name'],
         recipe_img = recipe_dict['image_url'],
         recipe_instructions = recipe_dict['instructions'],
         recipe_ingredients = recipe_dict['ingredients'],
        )


#Returns a list of saved recipes

@app.route('/saved_recipes',methods=['GET','POST'])
def saved_recipes():
    recipes = view_saved_recipes(current_user.username)
    return flask.render_template('saved_recipes.html', recipes=recipes)

# @app.route('/pull_saved_recipes')
#Call inside of saved recipes to get query
def view_saved_recipes(username):
    saved_recipes = Recipe.query.filter_by(username=username).all()
    return saved_recipes
    
@login_required
@app.route('/handle_save_recipe', methods=['GET','POST'])
def handle_save_recipe():
    #TODO:Save Username to send to database
    recipe_form = flask.request.form
    # recipe_user = recipe_form['username_field']
    recipe_user = current_user.username
    recipe_name = recipe_form['name']
    recipe_ingredients = recipe_form['ingredients']
    recipe_instructions = recipe_form['instructions']
    saved_rec = Recipe(username=recipe_user,recipe_name=recipe_name,recipe_ingredients=recipe_ingredients,recipe_instructions=recipe_instructions)
    db.session.add(saved_rec)
    db.session.commit()
    flask.flash("Recipe has been saved")
    return flask.redirect(flask.url_for('index_page'))



if __name__ == "__main__":
    app.run()