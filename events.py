import secrets
from db import db

def get_public_events():
    sql = """SELECT e.id, e.name, e.datetime, u.username,
            (SELECT COUNT(event_id) FROM enrolments WHERE event_id=e.id) FROM events e
            LEFT JOIN users u ON u.id=e.creator_id
            WHERE visible=TRUE AND private_key IS NULL
            AND (NOT e.datetime<NOW() OR e.datetime ISNULL) ORDER BY e.datetime"""

    events = db.session.execute(sql).fetchall()
    return events

def get_private_events(private_key):
    sql = """SELECT e.id, e.name, e.datetime, u.username FROM events e
            LEFT JOIN users u ON u.id=e.creator_id 
            WHERE visible=TRUE AND private_key=:private_key"""

    matches = db.session.execute(sql, {"private_key":private_key}).fetchall()
    return matches

def get_passed_events():
    sql = """SELECT e.id, e.name, e.datetime, u.username FROM events e
            LEFT JOIN users u ON u.id=e.creator_id
            WHERE visible=TRUE AND datetime<NOW() AND e.private_key IS NULL
            ORDER BY e.datetime"""

    return db.session.execute(sql).fetchall()

def get_passed_private_events(user_id):
    sql = """SELECT DISTINCT ev.id, ev.name, ev.datetime FROM events ev LEFT JOIN enrolments en
            ON ev.id=en.event_id WHERE (ev.creator_id=:user_id OR en.user_id=:user_id)
            AND ev.private_key IS NOT NULL AND ev.datetime<NOW() AND visible=TRUE 
            ORDER BY ev.datetime"""

    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_private_event(private_key):
    sql = "SELECT id from events where private_key=:private_key"
    event = db.session.execute(sql, {"private_key":private_key}).fetchone()
    
    return get_event(event.id)

def get_enrolled_events(user_id):
    sql = """SELECT ev.id, ev.name, ev.datetime,
            (SELECT username FROM users WHERE id=ev.creator_id),
            (SELECT COUNT(event_id) FROM enrolments WHERE event_id=ev.id) FROM events ev, enrolments en
            WHERE ev.id=en.event_id AND en.user_id=:user_id AND ev.visible=TRUE
            AND (NOT ev.datetime<NOW() OR ev.datetime ISNULL) ORDER BY ev.datetime"""
    enrolled_events = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return enrolled_events

def get_my_events(user_id):
    sql = """SELECT id, name, datetime, private_key,
        (SELECT COUNT(event_id) FROM enrolments WHERE event_id=events.id)
        FROM events WHERE creator_id=:user_id AND visible=TRUE
        AND (NOT datetime<NOW() OR datetime ISNULL) ORDER BY datetime"""
    my_events = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return my_events

def get_event(event_id):
    sql = """SELECT id, name, description, creator_id, datetime,
            location, private_key FROM events WHERE events.id = :event_id"""
    event = db.session.execute(sql, {"event_id": event_id}).fetchone()
    return event

def get_event_name(event_id):
    sql = "SELECT name FROM events WHERE id=:event_id"
    return db.session.execute(sql, {"event_id":event_id}).fetchone()[0]

def create_event(name, description, creator_id, datetime, location, private_key):
    sql = """INSERT INTO events (name, description, creator_id, datetime, location, private_key)
        VALUES (:name, :description, :creator_id, :datetime, :location, :private_key)"""
    db.session.execute(sql, {"name":name, "description":description,
                            "creator_id":creator_id, "datetime":datetime,
                            "location":location, "private_key":private_key})
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

def set_role(event_id, username, role):
    sql = "SELECT id FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()

    sql = "UPDATE enrolments SET role=:role WHERE event_id=:event_id AND user_id=:user_id"
    db.session.execute(sql, {"role":role, "event_id":event_id, "user_id":user.id})
    db.session.commit()

def cancel_enrolment(event_id, user_id):
    sql = "DELETE FROM enrolments WHERE event_id=:event_id AND user_id=:user_id"
    db.session.execute(sql, {"event_id":event_id, "user_id":user_id})
    db.session.commit()

def get_enrolments(event_id):
    sql = """SELECT DISTINCT u.username, e.role FROM users u, enrolments e
            WHERE u.id=e.user_id AND e.event_id=:event_id"""
    enr = db.session.execute(sql, {"event_id":event_id}).fetchall()
    return enr

def delete_event(event_id):
    sql = "UPDATE events SET visible=FALSE WHERE id=:event_id"
    db.session.execute(sql, {"event_id":event_id})
    db.session.commit()

def generate_private_key():
    return secrets.token_hex(16)

def check_rights(event_id, user_id):
    sql = "SELECT 1 FROM enrolments WHERE event_id=:event_id AND user_id=:user_id AND role=2"
    role = db.session.execute(sql, {"event_id":event_id, "user_id":user_id}).fetchone()

    sql = "SELECT 1 FROM events WHERE id=:event_id AND creator_id=:user_id"
    creator = db.session.execute(sql, {"event_id":event_id, "user_id":user_id}).fetchone()

    if role or creator:
        return True
    return False
