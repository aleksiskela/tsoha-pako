from db import db
from random import shuffle, sample

def get_event_tasks(event_id):
    sql = "SELECT t.id, t.task_name, u.username FROM tasks t LEFT JOIN users u ON t.volunteer=u.id WHERE event_id=:event_id ORDER BY t.id"
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
    
    return str(db.session.execute("SELECT event_id FROM tasks WHERE id=:task_id", {"task_id":task_id}).fetchone()[0])

def withdraw(task_id):
    sql = "UPDATE tasks SET volunteer=NULL WHERE id=:task_id"
    db.session.execute(sql, {"task_id":task_id})
    db.session.commit()

    return str(db.session.execute("SELECT event_id FROM tasks WHERE id=:task_id", {"task_id":task_id}).fetchone()[0])

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
        sql = "UPDATE tasks SET volunteer=u.id FROM (SELECT id FROM users WHERE username=:username) AS u WHERE tasks.id=:task"
        db.session.execute(sql, {"username":username, "task":task})
        db.session.commit()

    
