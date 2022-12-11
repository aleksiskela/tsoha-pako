from db import db

def get_event_messages(event_id):
    sql = """SELECT u.username, m.content, m.id FROM users u
        LEFT JOIN messages m ON u.id=m.user_id WHERE m.event_id=:event_id ORDER BY m.send_time"""
    result = db.session.execute(sql, {"event_id":event_id})
    return result.fetchall()

def send_message(content, user_id, event_id):
    sql = """INSERT INTO messages (content, user_id, event_id, send_time)
        VALUES (:content, :user_id, :event_id, NOW())"""
    db.session.execute(sql, {"content":content, "user_id":user_id, "event_id":event_id})
    db.session.commit()

def delete_message(message_id):
    sql = "UPDATE messages SET content='VIESTI POISTETTU' WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    