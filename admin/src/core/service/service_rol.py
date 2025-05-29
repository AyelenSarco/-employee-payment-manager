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


def list_roles():
    try:
        return Rol.query.all()
    except:
        return abort(500)
    

def get_rol_name(id):
    try:
        rol = Rol.query.get(id)
        return rol.name
    except:
        return abort(500)
