from src.core.database import db
from src.core.models import Permission
from flask import abort

def create_permission(**kwargs):
    try:
        permission = Permission(**kwargs)
        db.session.add(permission)
        db.session.commit()
        return permission   
    except:
        db.session.rollback()
        return abort(500)
    

def delete_permission(id):
    try:
        permission_db = Permission.query.get(id)
        if permission_db:
            db.session.delete(permission_db)
            db.session.commit()
            return True
        return None
    except:
        db.session.rollback()
        return abort(500)
    

