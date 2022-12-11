from db import db

def get_votables(event_id):
    sql = """SELECT a.id, a.item, COALESCE(b.sum, 0) sum, COALESCE(b.count, 0) count
        FROM votables a LEFT JOIN 
        (SELECT votable_id, sum(vote), count(vote) FROM votes GROUP BY votable_id) b 
        ON a.id=b.votable_id WHERE event_id=:event_id
        ORDER BY COALESCE(b.sum,0) DESC"""
    result = db.session.execute(sql, {"event_id":event_id})
    return result.fetchall()

def cast_vote(user_id, votable_id, vote):
    sql = "INSERT INTO votes (user_id, votable_id, vote) VALUES (:user_id, :votable_id, :vote)"
    db.session.execute(sql, {"user_id":user_id, "votable_id":votable_id, "vote":vote})
    db.session.commit()

def delete_vote(user_id, votable_id):
    sql = "DELETE FROM votes WHERE user_id=:user_id AND votable_id=:votable_id"
    db.session.execute(sql, {"user_id":user_id, "votable_id":votable_id})
    db.session.commit()

def delete_event_votes(event_id, user_id):
    sql = """DELETE FROM votes WHERE votable_id IN
        (SELECT id FROM votables WHERE event_id=:event_id)
        AND user_id=:user_id"""
    db.session.execute(sql, {"event_id":event_id, "user_id":user_id})
    db.session.commit()

def add_votable(item, event_id):
    sql = "INSERT INTO votables (item, event_id) VALUES (:item, :event_id)"
    db.session.execute(sql, {"item":item, "event_id":event_id})
    db.session.commit()

def delete_votable(votable_id):
    sql = "DELETE FROM votables WHERE id=:votable_id"
    db.session.execute(sql, {"votable_id":votable_id})
    db.session.commit()

def get_already_voted(user_id):
    sql = "SELECT votable_id FROM votes WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    already_voted = [votable.votable_id for votable in result]
    if already_voted is None:
        already_voted = []
    return already_voted
