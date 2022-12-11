from random import shuffle, sample, choice
from db import db

def get_event_tasks(event_id):
    sql = """SELECT t.id, t.task_name, u.username FROM tasks t
        LEFT JOIN users u ON t.volunteer=u.id WHERE event_id=:event_id ORDER BY t.id"""
    result = db.session.execute(sql, {"event_id":event_id})
    return result.fetchall()

def add_task(task_name, event_id):
    sql = "INSERT INTO tasks (task_name, event_id) VALUES (:task_name, :event_id)"
    db.session.execute(sql, {"task_name":task_name, "event_id":event_id})
    db.session.commit()

def set_volunteer(user_id, task_id):
    sql = "UPDATE tasks SET volunteer=:user_id WHERE tasks.id=:task_id"
    db.session.execute(sql, {"user_id":user_id, "task_id":task_id})
    db.session.commit()

    return str(db.session.execute("SELECT event_id FROM tasks WHERE id=:task_id",
                                    {"task_id":task_id}).fetchone()[0])

def withdraw(task_id):
    sql = "UPDATE tasks SET volunteer=NULL WHERE id=:task_id"
    db.session.execute(sql, {"task_id":task_id})
    db.session.commit()

    return str(db.session.execute("SELECT event_id FROM tasks WHERE id=:task_id",
                                    {"task_id":task_id}).fetchone()[0])

def randomize_all(event_id, enrolments):
    tasks = [task.id for task in get_event_tasks(event_id)]

    randomized = {}

    shuffle(enrolments)

    if len(enrolments) < len(tasks):
        for item in enrolments:
            enrolments.append(item)
            if len(enrolments) >= len(tasks):
                break

    enrolments = sample(enrolments, len(tasks))

    for i in range(len(tasks)):
        randomized[tasks[i]] = enrolments[i]

    for task, username in randomized.items():
        sql = """UPDATE tasks SET volunteer=u.id FROM
                (SELECT id FROM users WHERE username=:username) AS u
                WHERE tasks.id=:task"""
        db.session.execute(sql, {"username":username, "task":task})
        db.session.commit()

def randomize_unfilled(event_id):
    sql = "SELECT id, volunteer FROM tasks WHERE event_id=:event_id"
    query = db.session.execute(sql, {"event_id":event_id}).fetchall()
    sql = "SELECT user_id FROM enrolments WHERE event_id=:event_id"
    result = db.session.execute(sql, {"event_id":event_id}).fetchall()
    enrolments = [enrolment.user_id for enrolment in result]

    def randomize_remaining(query, enrolments):
        unfilled = [row for row in query if row[1] is None]
        if len(unfilled) == 0:
            return query

        tasks_per_user = {}

        for user in enrolments:
            tasks_per_user[user] = 0
            for row in query:
                if row[1] is not None:
                    if row[1] == user:
                        tasks_per_user[user] += 1

        laziest = [user for user, tasks in tasks_per_user.items() \
                    if tasks == min(tasks_per_user.values())]
        shuffle(laziest)

        while len(laziest) > 0 and len(unfilled) > 0:
            assignable = choice(unfilled)
            unfilled.remove(assignable)
            assign = (assignable[0], laziest.pop(0))
            query.remove(assignable)
            query.append(assign)

        return randomize_remaining(query, enrolments)

    randomized = randomize_remaining(query, enrolments)

    for task in randomized:
        set_volunteer(task[1], task[0])

def delete_task(task_id):
    sql = "DELETE FROM tasks WHERE id=:task_id"
    db.session.execute(sql, {"task_id":task_id})
    db.session.commit()

def withdraw_event_tasks(event_id, user_id):
    sql = "UPDATE tasks SET volunteer=NULL WHERE event_id=:event_id AND volunteer=:user_id"
    db.session.execute(sql, {"event_id":event_id, "user_id":user_id})
    db.session.commit()