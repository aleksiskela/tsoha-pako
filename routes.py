from app import app
from flask import render_template, request, redirect
import events
import users
import messages

@app.route("/")
def index():
    return render_template("index.html", events=events.get_all_events())


@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    
    enrolment_data = events.get_enrolments(event_id)
    enrolments = [user.username for user in enrolment_data]

    name = event.name
    description = event.description
    creator_id = event.creator_id
    creator_username = users.get_username(creator_id)
    
    return render_template("event.html", name=name, description=description, id=event_id, creator_username=creator_username, enrolments=enrolments)


@app.route("/create_event", methods=["GET","POST"])
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        creator = users.get_my_id()

        if len(name) > 100:
            return render_template("error.html", message="Tapahtuman nimessä saa olla korkeintaan 100 merkkiä")
        if len(name.strip()) < 1:
            return render_template("error.html", message="Tapahtuman nimessä on oltava vähintään yksi merkki")
        if len(description) > 10000:
            return render_template("error.html", message="Tapahtuman kuvauksessa saa olla korkeintaan 10 000 merkkiä")
        if len(description) == 0:
            description = "Tapahtumalla ei ole kuvausta"

        events.create_event(name, description, creator)
    
    return redirect("/")

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = request.form["event_id"]
    events.delete_event(event_id)
    return redirect("/")

@app.route("/enrol", methods=["POST"])
def enrol():
    event_id = request.form["event_id"]
    role = request.form["role"]
    user_id = users.get_my_id()

    events.enrol(event_id, user_id, role)

    return redirect(f"/event/{event_id}")

@app.route("/leave_event", methods=["POST"])
def cancel_enrolment():
    event_id = request.form["event_id"]
    user_id = users.get_my_id()

    events.cancel_enrolment(event_id, user_id)

    return redirect(f"/event/{event_id}")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return render_template("/error.html", message="Tunnus tai salasana väärin")

    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_check = request.form["password_check"]

        if users.username_exists(username):
            return render_template("error.html", message="Käyttäjätunnus varattu")

        if password != password_check:
            return render_template("error.html", message="Salasanat eivät täsmää")

        if not 3 <= len(username) <= 20 or not 3 <= len(password) <= 30:
            return render_template("error.html", message="Yritit kiertää")

        users.register(username, password)

        return redirect("/")

@app.route("/messages/<int:event_id>", methods=["GET", "POST"])
def show_messages(event_id):
    if request.method == "GET":
        event_messages = messages.get_event_messages(event_id)

        return render_template("messages.html", messages=event_messages)

    if request.method == "POST":
        content = request.form["content"]
        user_id = users.get_my_id()
        
        messages.send_message(content, user_id, event_id)
        event_messages = messages.get_event_messages(event_id)
    
    return render_template("/messages.html", messages=event_messages)