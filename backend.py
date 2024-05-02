from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

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
@app.route("/", methods=["GET", "POST"])
def intro():
    if request.method == "GET":
        return render_template("intro.html")
    elif request.method == "POST":
        #print(request.form) # Debug
        action = request.form.get("action") # Using .get() to avoid a KeyError
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return jsonify({"error": "Missing username."})
        if not password:
            return jsonify({"error": "Missing password."})
        
        if action == "login":
            with app.app_context():
                engine = db.get_engine('dbauth')
                with engine.connect() as connection:
                    sql = text("SELECT passhash FROM userauth WHERE username=:username")
                    result = connection.execute(sql, {"username":username})
                    user = result.fetchone()
                    if not user: 
                        # Invalid username
                        return jsonify({"error": "Username does not exist."})
                    else:
                        passhash = user.password
                        if check_password_hash(passhash, pepper + password): # Correct, log in
                            session["username"] = username
                        else:
                            # Invalid password
                            return jsonify({"error": "Password is incorrect."})
        elif action == "signup":
            passhash = generate_password_hash(pepper + password)
            return jsonify({"message": "Signup successful! Now login to verify."})
        else:
            return jsonify({"error": "Missing password."})


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
def groups():
    return render_template("groups.html")


'''
[[Dev notes]]


[To access the binded db url I can use]

with app.app_context():
    engine = db.get_engine('dbauth')
    with engine.connect() as connection:
        result = connection.execute('SELECT * FROM userauth')

'''


