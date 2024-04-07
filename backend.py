from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL_AUTH")
db_auth = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db_content = SQLAlchemy(app)
db = SQLAlchemy(app)

pepper = getenv("DATABASE_PEPPER")

@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # tbd. authentication logic
        pass
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # tbd. registration logic
        pass
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", username=username)

@app.route("/dms")
def dms():
    return render_template("dms.html")
