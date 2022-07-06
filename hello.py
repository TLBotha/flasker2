from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "super secret key"

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