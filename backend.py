from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session, jsonify, abort, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

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
        if len(password) < 8:
            return jsonify({"error": "Password must be longer"})
        
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
                        passhash = user.passhash
                        if check_password_hash(passhash, pepper + password): # Correct, log in
                            sql = text("SELECT id FROM users WHERE username=:username")
                            result = db.session.execute(sql, {"username":username})
                            user = result.fetchone()
                            if not user:
                                sql = text("INSERT INTO users (username, permission, displayname, created_at) VALUES (:username, 0, 'Anonymoose', NOW())")
                                db.session.execute(sql, {"username":username})
                                db.session.commit()
                            session["username"] = username
                            session["crsf_token"] = token_hex(16)
                            return jsonify({"success": "1"})
                        else:
                            # Invalid password
                            return jsonify({"error": "Password is incorrect."})
        elif action == "signup":
            sql = text("SELECT id FROM users WHERE username=:username")
            result = db.session.execute(sql, {"username":username})
            user = result.fetchone()
            if user:
                return jsonify({"error": "Username already exists."}) 
            passhash = generate_password_hash(pepper + password)
            with app.app_context():
                engine = db.get_engine('dbauth')
                with engine.connect() as connection:
                    sql = text("""
                        INSERT INTO userauth (username, passhash) 
                        VALUES (:username, :passhash)
                        ON CONFLICT (username) 
                        DO UPDATE SET passhash = :passhash, publickey = NULL, privatekey = NULL
                        """)
                    connection.execute(sql, {"username":username, "passhash":passhash})
                    connection.commit()
            return jsonify({"message": "Signup successful! Now login to verify."})
        else:
            return jsonify({"error": "Missing password."})



# New landing page once logged in - the home of posts
@app.route("/home", methods=["GET", "POST"])
def home():
    if not session.get("username"):
        return render_template("home.html")
    if request.method == "GET":
        if request.args.get("query"):
            lookup = True
            sql = text("""
                SELECT users.username, content.id, content.created_at, content.content, COUNT(DISTINCT content_likes.id) AS likes,
                CASE WHEN COUNT(user_likes.id) > 0 THEN TRUE ELSE FALSE END AS liked
                FROM content
                LEFT JOIN users ON users.id = content.user_id
                LEFT JOIN content_likes ON content_likes.content_id = content.id
                LEFT JOIN content_likes AS user_likes ON user_likes.content_id = content.id AND user_likes.liker_id = (SELECT id FROM users WHERE username = :username)
                WHERE content.public = True AND content.category = 'post' AND content.content LIKE :query
                GROUP BY users.username, content.id
                """)
            result = db.session.execute(sql, {"username": session["username"], "query": "%"+request.args.get("query")+"%"})
        else:
            lookup = None
            sql = text("""
                SELECT users.username, content.id, content.created_at, content.content, COUNT(DISTINCT content_likes.id) AS likes,
                CASE WHEN COUNT(user_likes.id) > 0 THEN TRUE ELSE FALSE END AS liked
                FROM content
                LEFT JOIN users ON users.id = content.user_id
                LEFT JOIN content_likes ON content_likes.content_id = content.id
                LEFT JOIN content_likes AS user_likes ON user_likes.content_id = content.id AND user_likes.liker_id = (SELECT id FROM users WHERE username = :username)
                WHERE content.public = True AND content.category = 'post'
                GROUP BY users.username, content.id
                """)
            result = db.session.execute(sql, {"username": session["username"]})
        items = result.fetchall()
        return render_template("home.html", posts=items, search=lookup, query=request.args.get("query"))
    elif request.method == "POST":
        print(request.form)
        if session.get("crsf_token") != request.form.get("crsf_token"):
            abort(403)
        action = request.form.get("action")
        if action == "newpost":
            content = request.form.get("text")
            files = request.form.get("files") # Work in progress
            if len(content) > 1000:
                return jsonify({"error": "Message too long."})
            sql = text("""
                INSERT INTO content (user_id, category, content, public, created_at)
                VALUES ((SELECT id FROM users WHERE username = :username), 'post', :text, True, NOW())
                """)
            db.session.execute(sql, {"username": session["username"], "text":content})
            db.session.commit()
            return jsonify({"message": "Successful post."})
        elif action == "heart":
            print("WE GOT A HEART")
            post_id = request.form.get("post_id")
            if not post_id:
                abort(400)
            sql = text("""
                INSERT INTO content_likes (content_id, liker_id)
                VALUES (:post_id, (SELECT id FROM users WHERE username = :username))
                """)
            db.session.execute(sql, {"username": session["username"], "post_id": post_id})
            db.session.commit()
            print("HEARTED")
            return Response(status=204)
        elif action == "unheart":
            post_id = request.form.get("post_id")
            if not post_id:
                abort(400)
            sql = text("""
                DELETE FROM content_likes 
                WHERE content_id = :post_id AND liker_id = (SELECT id FROM users WHERE username = :username)
                """)
            db.session.execute(sql, {"username": session["username"], "post_id": post_id})
            db.session.commit()
            return Response(status=204)



# Profile page for usernames. Shows different details depending if it's your profile page or not.
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if not session.get("username"):
        return render_template("profile.html")
    if request.method == "GET":
        sql = text("""
            SELECT users.bio, users.displayname, users.created_at, media.id as pfp
            FROM users
            LEFT JOIN media ON users.pfp = media.id
            WHERE users.username=:username
            """)
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return redirect(f"/profile/{session.get('username')}")
        yourself = None
        if session.get("username") == username:
            yourself = True
        return render_template("profile.html", username=username, bio=user.bio, myself=yourself, name=user.displayname, joined=user.created_at, pfp=user.pfp)
    elif request.method == "POST":
        if session.get("crsf_token") != request.form.get("crsf_token"):
            abort(403)
        file = request.files["file"]
        name = file.filename
        if not name.endswith(".jpg"):
            return jsonify({"error": "File must be .jpg"})
        data = file.read()
        if len(data) > 8000*1024:
            return jsonify({"error": "Max filesize is 8 Mb."})
        sql = text("INSERT INTO media (media_type, media_data, created_at) VALUES ('jpg', :data, NOW()) RETURNING id")
        result = db.session.execute(sql, {"data":data})
        db.session.commit()
        media_id = result.fetchone()[0]
        sql = text("UPDATE users SET pfp = :media_id WHERE username = :username")
        db.session.execute(sql, {"media_id": media_id, "username": session.get('username')})
        db.session.commit()
        return jsonify({"message": "Upload success, refresh page."})


@app.route("/messages")
def dms():
    return render_template("messages.html")

@app.route("/groups")
def groups():
    return render_template("groups.html")

# Link for images (course material)
@app.route('/image/<id>')
def show(id):
    sql = text("SELECT media_data FROM media WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

# Log out
@app.route("/logout")
def logout():
    if session.get("username"):
        del session["username"]
    if session.get("crsf_token"):
        del session["crsf_token"]
    return redirect("/")

