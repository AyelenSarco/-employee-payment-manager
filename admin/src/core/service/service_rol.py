from flask import abort
from src.core.database import db
from src.core.models import Rol

def create_rol(**kwargs):
    try:
        rol = Rol(**kwargs)
        db.session.add(rol)
        db.session.commit()
        return rol
    except:
        db.session.rollback()
        return abort(500)

