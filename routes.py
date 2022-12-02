from datetime import datetime
from flask import render_template, request, redirect
from app import app
import events
import users
import messages
import voting
import tasks

@app.route("/")
def index():
    return render_template("index.html", events=events.get_all_events())


@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)

    # enrolment_data = events.get_enrolments(event_id)
    # enrolments = [user.username for user in enrolment_data]
    enrolments = events.get_enrolments(event_id)

    name = event.name
    description = event.description
    creator_id = event.creator_id
    creator_username = users.get_username(creator_id)
    location = event.location

    if not location:
        location = "-"
    if len(location) == 0:
        location = "-"

    date = "-"
    time = "-"
    countdown = "-"

    try:
        timestamp = event.datetime
        date = timestamp.strftime("%d.%m.%y")
        time = timestamp.strftime("%H:%M")
        countdown = timestamp.date()-datetime.today().date()
        countdown = countdown.days


    except:
        pass

    return render_template("event.html", name=name, description=description, event_id=event_id,
                            creator_username=creator_username, enrolments=enrolments, date=date,
                            time=time, location=location, countdown=countdown)


@app.route("/create_event", methods=["GET","POST"])
def create_event():
    if request.method == "GET":
        return render_template("create_event.html")

    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        description = request.form["description"]
        creator = users.get_my_id()

        date = request.form["date"]
        time = request.form["time"]
        timestamp = date + " " + time
        if len(timestamp) == 1:
            timestamp = None

        location = request.form["location"]

        if len(name) > 100:
            return render_template("error.html",
                                    message="Tapahtuman nimessä saa olla korkeintaan 100 merkkiä")
        if len(name.strip()) < 1:
            return render_template("error.html",
                                    message="Tapahtuman nimessä on oltava vähintään yksi merkki")
        if len(description) > 2000:
            return render_template("error.html",
                                message="Tapahtuman kuvauksessa saa olla korkeintaan 2000 merkkiä")
        if len(description) == 0:
            description = "Tapahtumalla ei ole kuvausta"
        if len(location) > 100:
            return render_template("error.html",
                                    message="Paikkatieto saa olla korkeintaan 100 merkkiä")

        events.create_event(name, description, creator, timestamp, location)

    return redirect("/")

@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if request.method == "GET":
        event = events.get_event(event_id)
        name = event.name

        try:
            timestamp = event.datetime
            date = timestamp.date()
            time = timestamp.time()
        except AttributeError:
            date = ""
            time = ""

        return render_template("edit_event.html", event_id=event_id,
                                event=event, name=name, date=date, time=time)

    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        description = request.form["description"]

        date = request.form["date"]
        time = request.form["time"]
        timestamp = date + " " + time

        if len(timestamp) == 1:
            timestamp = None

        location = request.form["location"]

        if len(name) > 100:
            return render_template("error.html",
                                    message="Tapahtuman nimessä saa olla korkeintaan 100 merkkiä")
        if len(name.strip()) < 1:
            return render_template("error.html",
                                    message="Tapahtuman nimessä on oltava vähintään yksi merkki")
        if len(description) > 2000:
            return render_template("error.html",
                                message="Tapahtuman kuvauksessa saa olla korkeintaan 2000 merkkiä")
        if len(description) == 0:
            description = "Tapahtumalla ei ole kuvausta"
        if len(location) > 100:
            return render_template("error.html",
                                    message="Paikkatieto saa olla korkeintaan 100 merkkiä")

        events.edit_event(event_id, name, description, timestamp, location)

    return redirect("/event/"+str(event_id))

@app.route("/delete_event", methods=["POST"])
def delete_event():
    users.check_csrf()
    event_id = request.form["event_id"]
    events.delete_event(event_id)
    return redirect("/")

@app.route("/enrol", methods=["POST"])
def enrol():
    users.check_csrf()
    event_id = request.form["event_id"]
    role = request.form["role"]
    user_id = users.get_my_id()

    events.enrol(event_id, user_id, role)

    return redirect(f"/event/{event_id}")

@app.route("/leave_event", methods=["POST"])
def cancel_enrolment():
    users.check_csrf()
    event_id = request.form["event_id"]
    user_id = users.get_my_id()

    events.cancel_enrolment(event_id, user_id)

    return redirect(f"/event/{event_id}")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if not users.login(username, password):
        return render_template("/error.html",
                                message="Tunnus tai salasana väärin")

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
            return render_template("error.html",
                                    message="Käyttäjätunnus varattu")

        if password != password_check:
            return render_template("error.html",
                                    message="Salasanat eivät täsmää")

        if not 3 <= len(username) <= 20 or not 3 <= len(password) <= 30:
            return render_template("error.html",
                                message="""Käyttäjätunnuksessa oltava 3-20 merkkiä
                                ja salasanassa 3-30 merkkiä""")

        users.register(username, password)

        return redirect("/")

@app.route("/messages/<int:event_id>", methods=["GET", "POST"])
def show_messages(event_id):
    # if request.method == "GET":
    #     event_messages = messages.get_event_messages(event_id)

    #     return render_template("messages.html", messages=event_messages)

    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        user_id = users.get_my_id()

        if not 1 <= len(content) <= 100:
            return render_template("error.html",
                                    message="Viestissä oltava 1-100 merkkiä")

        messages.send_message(content, user_id, event_id)

    event_messages = messages.get_event_messages(event_id)
    enrolments = events.get_enrolments(event_id)
    name = events.get_event_name(event_id)

    return render_template("/messages.html", messages=event_messages,
                            enrolments=enrolments, event_id=event_id, name=name)

@app.route("/voting/<int:event_id>", methods=["GET","POST"])
def show_votes(event_id):
    if request.method == "POST":
        users.check_csrf()
        votable_id = int(request.form["votable_id"])
        vote = request.form["vote"]
        if vote == "Jaa":
            vote = 1
        elif vote == "Ei":
            vote = -1
        elif vote == "Vaihda":
            voting.delete_vote(users.get_my_id(), votable_id)

        if vote != "Vaihda":
            voting.cast_vote(users.get_my_id(), votable_id, vote)


    event_votables = voting.get_votables(event_id)
    enrolments = events.get_enrolments(event_id)
    name = events.get_event_name(event_id)

    try:
        already_voted = voting.get_already_voted(users.get_my_id())
    except KeyError:
        already_voted = []


    return render_template("voting.html", votables=event_votables,
                        already_voted=already_voted, event_id=event_id,
                        enrolments=enrolments, name=name)

@app.route("/add_votable", methods=["POST"])
def add_votable():
    users.check_csrf()
    item = request.form["item"]
    event_id = request.form["event_id"]

    if not 1 <= len(item) <= 50:
        return render_template("error.html",
                                message="Kohteen nimen oltava 1-50 merkkiä")

    voting.add_votable(item, event_id)

    return redirect("/voting/"+event_id)

@app.route("/tasks/<int:event_id>")
def show_tasks(event_id):
    event_tasks = tasks.get_event_tasks(event_id)
    enrolments = events.get_enrolments(event_id)
    name = events.get_event_name(event_id)

    return render_template("tasks.html", event_tasks=event_tasks,
                            event_id=event_id, enrolments=enrolments, name=name)

@app.route("/set_volunteer", methods=["POST"])
def set_volunteer():
    users.check_csrf()
    task_id = int(request.form["task_id"])
    user_id = users.get_my_id()

    event_id = tasks.set_volunteer(user_id, task_id)

    return redirect("/tasks/"+event_id)

@app.route("/withdraw", methods=["POST"])
def withdraw():
    users.check_csrf()
    task_id = int(request.form["task_id"])

    event_id = tasks.withdraw(task_id)

    return redirect("/tasks/"+event_id)

@app.route("/new_task", methods=["POST"])
def add_task():
    users.check_csrf()
    task = request.form["task"]
    event_id = request.form["event_id"]

    if not 1 <= len(task) <= 50:
        return render_template("error.html",
                                message="Tehtävän nimen oltava 1-50 merkkiä")

    tasks.add_task(task, event_id)

    return redirect("/tasks/"+event_id)

@app.route("/randomize_all", methods=["POST"])
def randomize_all():
    users.check_csrf()
    event_id = request.form["event_id"]
    enrolments = events.get_enrolments(event_id)

    tasks.randomize_all(event_id, enrolments)

    return redirect("/tasks/" + event_id)

@app.route("/randomize_unfilled", methods=["POST"])
def randomize_unfilled():
    users.check_csrf()
    event_id = request.form["event_id"]
    tasks.randomize_unfilled(event_id)

    return redirect("/tasks/" + event_id)
