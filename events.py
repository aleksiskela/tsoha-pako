from db import db

def get_all_events():
    sql = db.session.execute("""SELECT e.id, e.name, u.username FROM events e
                            LEFT JOIN users u ON u.id=e.creator_id WHERE visible=TRUE""")
    events = sql.fetchall()
    return events

def get_event(event_id):
    sql = """SELECT id, name, description, creator_id, datetime,
            location FROM events WHERE events.id = :event_id"""
    event = db.session.execute(sql, {"event_id": event_id}).fetchone()
    return event

def get_event_name(event_id):
    sql = "SELECT name FROM events WHERE id=:event_id"
    return db.session.execute(sql, {"event_id":event_id}).fetchone()[0]

def create_event(name, description, creator_id, datetime, location):
    sql = """INSERT INTO events (name, description, creator_id, datetime, location)
        VALUES (:name, :description, :creator_id, :datetime, :location)"""
    db.session.execute(sql, {"name":name, "description":description,
                            "creator_id":creator_id, "datetime":datetime, "location":location})
    db.session.commit()

def edit_event(event_id, name, description, datetime, location):
    sql = """UPDATE events SET name=:name, description=:description,
        datetime=:datetime, location=:location WHERE id=:event_id"""
    db.session.execute(sql, {"event_id": event_id, "name":name,
                            "description":description, "datetime":datetime, "location":location})
    db.session.commit()

def enrol(event_id, user_id, role):
    sql = "INSERT INTO enrolments (event_id, user_id, role) VALUES (:event_id, :user_id, :role)"
    db.session.execute(sql, {"event_id":event_id, "user_id":user_id, "role":role})
    db.session.commit()

def cancel_enrolment(event_id, user_id):
    sql = "DELETE FROM enrolments WHERE event_id=:event_id AND user_id=:user_id"
    db.session.execute(sql, {"event_id":event_id, "user_id":user_id})
    db.session.commit()

def get_enrolments(event_id):
    sql = """SELECT DISTINCT u.username FROM users u, enrolments e
            WHERE u.id=e.user_id AND e.event_id=:event_id"""
    result = db.session.execute(sql, {"event_id":event_id}).fetchall()
    enrolments = [user.username for user in result]
    return enrolments

def delete_event(event_id):
    sql = "UPDATE events SET visible=FALSE WHERE id=:event_id"
    db.session.execute(sql, {"event_id":event_id})
    db.session.commit()
