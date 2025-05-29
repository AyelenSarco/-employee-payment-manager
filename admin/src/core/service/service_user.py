from flask import abort
from src.core.database import db
from src.core.models import User, Permission,Rol
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
    
def list_users(email = None, rol_id = None, sort_by = 'name', sort_order = 'asc', pag = 1):
    try:
        users = User.query.filter_by()

        if email and email != '':
            users = users.filter(User.email.ilike(f'%{email}'))

        if rol_id and rol_id != '':
            users = users.filter_by(rol_id=rol_id)
        
        if sort_by == 'name':
            users = users.order_by(User.name.asc() if sort_order == 'asc' else User.name.desc())
        elif sort_by =="email":
            users = users.order_by(User.email.asc()if sort_order == 'asc' else User.email.desc())
        else: 
            users = users.order_by(User.creation_date.asc() if sort_order ==  'asc' else User.creation_date.desc())

        users = users.paginate(page = pag, per_page=2)

        return users
    except:
        return abort(500)
    

def search_user_by_email(email):
    try:
        return User.query.filter_by(email=email).first()
    except:
        abort(500)

def validate_password(id, password):
    try:
        user_db = User.query.get(id)
        if user_db:
            return check_password_hash(user_db.hashed_password, password)
        return False
    except:
        return abort(500)


def get_permissions(id):
    try:
        permissions = db.session.query(Permission.name).join(Rol.permissions).join(User) \
                    .filter(User.rol_id == Rol.id, User.id == id).all
        
        return [ permission.name for permission in permissions]
    except:
        abort(500)
    

def update_user(id, new_data):
    try:
        user = User.query.get(id)
        if (new_data.get('name')):
            user.name = new_data['name']
        if (new_data.get('rol_id')):
            user.rol_id = new_data['rol_id']
        if ( new_data.get('email')):
            user.email = new_data['email']
        if(new_data.get('sys_admin')):
            user.sys_admin = new_data['sys_admin']
        if(new_data.get('is_active')):
            user.is_active = new_data['is_active']
        
        db.session.commit()
        return user
    except:
        db.session.rollback()
        return abort(500)