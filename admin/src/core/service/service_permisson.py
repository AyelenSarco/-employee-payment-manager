from src.core.database import db
from src.core.models import Permisson
from flask import abort

def create_permisson(**kwargs):
    try:
        permisson = Permisson(**kwargs)
        db.session.add(permisson)
        db.session.commit()
        return permisson   
    except:
        db.session.rollback()
        return abort(500)
    

def delete_permisson(id):
    try:
        permisson_db = Permisson.query.get(id)
        if permisson_db:
            db.session.delete(permisson_db)
            db.session.commit()
            return True
        return None
    except:
        db.session.rollback()
        return abort(500)
    

