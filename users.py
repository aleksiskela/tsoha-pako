import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, abort, request
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
        else:
            return False
    else:
        return False
    return True

def logout():
    del session["username"]

def username_exists(username):
    sql = "SELECT id FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    if user:
        return True
    return False

def register(username, password):
    hash_value = generate_password_hash(password)

    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()

    return login(username, password)

def get_all_users():
    sql = "SELECT username FROM users"
    all_users = db.session.execute(sql).fetchall()
    for user in all_users:
        print(user.username)

def get_my_id():
    username = session["username"]
    sql = "SELECT id FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    return user.id

def get_username(user_id):
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id}).fetchone()
    return result.username

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def delete_account(user_id):
    sql = "UPDATE users SET password='' WHERE id=:user_id"
    db.session.execute(sql, {"user_id":user_id})
    