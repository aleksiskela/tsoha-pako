from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = db.session.execute("SELECT id, name FROM events")
    events = sql.fetchall()
    print("Testi")
    return render_template("index.html", events=events)

@app.route("/event/<int:event_id>")
def show_event(event_id):
    sql = "SELECT name, description FROM events WHERE events.id = :event_id"
    # name = db.session.execute(sql, {"event_id": event_id}).fetchone()
    # print(name[0])
    # description = db.session.execute(sql, {"event_id": event_id}).fetchone()[1]
    event = db.session.execute(sql, {"event_id": event_id}).fetchone()
    print(event)
    name = event[0]
    description = event[1]
    
    return render_template("event.html", name=name, description=description)
    # return render_template("event.html", name=name)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            return render_template("/login_error.html", message="Username or password incorrect")

    else:
        return render_template("/login_error.html", message="Username or password incorrect")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_check = request.form["password_check"]

        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if user:
            print("Username taken")
            # return redirect("/login_error", message="Username taken")
            return render_template("login_error.html", message = "Username taken")

        if password != password_check:
            print("Password mismatch")
            # return redirect("/login_error")
            return render_template("login_error.html", message="Password mismatch")

        if not 3 <= len(username) <= 20 or not 3 <= len(password) <= 30:
            print("Yritit kiertää")
            # return redirect("/login_error")
            return render_template("login_error.html", message="Yritit kiertää")


        hash_value = generate_password_hash(password)

        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()

        return redirect("/")

# @app.route("/login_error")
# def login_error(message):
#     return render_template("login_error.html")

@app.route("/create_event", methods=["GET","POST"])
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        sql = "SELECT id FROM events WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        event = result.fetchone()

        if event:
            print("Event name taken")
            # return redirect("/login_error")
            return render_template("login_error.html", message="Event name taken")

        else:
            sql = "INSERT INTO events (name, description) VALUES (:name, :description)"
            db.session.execute(sql, {"name":name, "description":description})
            db.session.commit()
    
    return redirect("/")