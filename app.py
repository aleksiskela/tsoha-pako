from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key=getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = db.session.execute("SELECT id, name FROM events")
    events = sql.fetchall()
    return render_template("index.html", events=events)

@app.route("/event/<int:event_id>")
def show_event(event_id):
    sql = "SELECT name FROM events WHERE events.id = :event_id"
    name = db.session.execute(sql, {"event_id": event_id}).fetchone()[0]
    return render_template("event.html", name=name)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    # password = request.form["password"]

    session["username"] = username

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
        sql = "INSERT INTO users (username) VALUES (:username)"
        db.session.execute(sql, {"username": username})
        db.session.commit()

        return redirect("/")