from flask import abort
from src.core.database import db
from src.core.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import traceback

def create_user(**kwargs):
    try:
        kwargs['hashed_password'] = generate_password_hash(kwargs['hashed_password'])
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    except:
        db.session.rollback()
        traceback.print_exc()
        return abort(500)

def get_user(id):
    try:
        user = User.query.get(id)
        return user
    except:
        return abort(500)
    
def edit_user(id, new_data):
    try:
        user = User.query.get(id)
        if(new_data.get('name')):
            user.name = new_data['name']
        db.session.commit()
        return user
    except:
        db.session.rollback()
        return abort(500)
    
def delete_user(id):
    try:
        user_db = User.query.get(id)
        if user_db:
            if user_db.sys_admin:
                return False
            db.session.delete(user_db)
            db.session.commit()
            return True
        return None
    except:
        db.session.rollback()
        return abort(500)
    
def list_users():
    try:
        users = User.query(User).all()
        return users
    except:
        return abort(500)