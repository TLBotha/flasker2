from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = "super secret key"
# Initialize The Database
db = SQLAlchemy(app) 

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')

# def index():
#    return "<h1> Hello World </h1>"

# JINJA FILTERS !!
# safe (allow html to be passed with variable)
# capatilize ()
# lower
# upper
# title (Capatilize every word in sentence)
# trim (remove trailing spaces)
# striptags (remove html tags)

def index():
    name = "Theunis"
    stuff = "This is <strong>Bold</strong>"
    # list
    favorite_pizza = ["Ppperoni", "Cheese", "Mushroom", 41]

    return render_template("index.html", 
        name=name,
        stuff=stuff,
        favorite_pizza=favorite_pizza
        )
    
@app.route('/user/add_user', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
    form=form,
    name=name,
    our_users=our_users)

# localhost:5000/user/Theunis
@app.route('/user/<name>')

def user(name):
    # return "<h1> Hello {}</h1>".format(name)
    return render_template("user.html", name=name)

# Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template("name.html",
        name = name,
        form = form)