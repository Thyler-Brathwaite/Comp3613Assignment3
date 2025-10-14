from App.models import User,LoggedHours,Request
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def get_all_requests():
    return db.session.scalars(db.select(Request)).all()

def get_all_requests_json():
    requests = get_all_requests()
    if not requests:
        return []
    requests = [request.get_json() for request in requests]
    return requests

def get_all_loggedhours():
    return db.session.scalars(db.select(LoggedHours)).all()

def get_all_loggedhours_json():
    logs = get_all_loggedhours()
    if not logs:
        return []
    logs = [log.get_json() for log in logs]
    return logs