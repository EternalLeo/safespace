from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

# Setting up the environment
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

# Storing the (application data) database as typical, the authentification table accesss as a bind.
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config['SQLALCHEMY_BINDS'] = {
    'dbauth': getenv("DATABASE_URL_AUTH")
}
db = SQLAlchemy(app)

# Secret environment variable pepper in addition to salt in-case database gets leaked
pepper = getenv("DATABASE_PEPPER")

# Landing page
# Signing up and logging in happens here - so subsite link for ease of css animation
@app.route("/")
def intro():
    return render_template("intro.html")

# This section will be deleted, since the post belongs to the above
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # tbd. authentication logic
        pass
    return render_template("login.html")

# Following section is very much placeholder!
# In the main site
# (On top for PC)
#
#
# (On bottom for mobile)
# [Navbar] -> Feed, Messages, Groups, Profile

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", username=username)

@app.route("/messages")
def dms():
    return render_template("messages.html")

@app.route("/groups")
def dms():
    return render_template("groups.html")


'''
[[Dev notes]]


[To access the binded db url I can use]

with app.app_context():
    engine = db.get_engine(app, 'dbauth')
    result = engine.execute('SELECT * FROM userauth')

'''


