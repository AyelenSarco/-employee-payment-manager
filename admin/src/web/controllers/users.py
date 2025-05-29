from flask import Blueprint, render_template, url_for, redirect,request, abort, flash
from src.core.service.service_user import create_user,get_user, list_users, delete_user, update_user
from src.core.service.service_rol import list_roles, get_rol_name
from src.web.handlers.auth import login_required,check
from datetime import datetime
import traceback

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.get("/")
@login_required
@check("user_list")
def index():
    try:
        pag = request.args.get('pag',1 , type = int)
        email = request.args.get("email", type= str)
        if email:
            email = email.strip()
        rol_id = request.args.get('rol_id',None,type= int)
        sort_by = request.args.get('sort_by','name')
        sort_order = request.args.get('sort_order','asc')
        users = list_users(email, rol_id,sort_by,sort_order, pag)
        
        
        return render_template('users/index.html', users = users)
    except:
        traceback.print_exc()
        return abort(400)
    
@bp.route("/new", methods=['GET','POST'])
@login_required
@check("user_create")
def create():
    try:
        roles = list_roles()
        today = datetime.today().date().isoformat()

        if(request.method == 'POST'):
            data = request.form
            is_sys_admin = 'sys_admin' in data
            is_active = 'state' in data

            new_user = {
                "name": data['name'],
                "email": data['email'].strip(),
                "hashed_password": data['password'],
                "is_active": is_active,
                "creation_date": data['creation_date'],
                "sys_admin": is_sys_admin,
                "rol_id": data['rol'],
            }

            # TO DO : Validate data
            valid_data = True
            if valid_data:
                create_user(**new_user)
                flash('User created successfully','sucess')
                return redirect(url_for('users.index'))
            
            
            return render_template('users/create_user.html', roles=roles, today=today, new_user=new_user)


        return render_template('users/create_user.html', roles = roles, today=today)
        
    except:
        traceback.print_exc()
        return abort(400)
    

@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@check('user_delete')
def delete(user_id):
    try:
        deleted = delete_user(user_id)
        if deleted is True:
            flash('User successfully deleted', 'succes')
        elif deleted is False:
            flash('You cannot delete a user with Sys Admin privileges.','error')
        else:
            flash('User not found','error')
        return redirect(url_for('users.index'))
    
    except:
        return abort(400)
    

@bp.route('/user/<int:user_id>')
@login_required
@check("user_view")
def view_user(user_id):
    try:
        user = get_user(user_id)
        rol_name = get_rol_name(user.rol_id)

        return render_template("/users/show_user.html", user=user, rol_name=rol_name)
    
    except:
        traceback.print_exc()
        return abort(400)
    

@bp.route('/edit/<int:user_id>')
@login_required
@check("user_edit")
def edit(user_id):
    try:
        roles = list_roles()
        user = get_user(user_id)
        return render_template('users/edit_user.html', user=user, roles=roles)

    except:
        traceback.print_exc()
        return abort(400)
    
@bp.route('/update/<int:user_id>', methods=['POST'])
@login_required
@check('user_edit')
def update(user_id):
    try:
        data = request.form
        is_sys_admin = 'sys_admin' in data
        is_active = 'state' in data
        
        new_data = {
            "name": data['name'],
            "rol_id": data['rol'],
            "email": data['email'],
            "sys_admin": is_sys_admin,
            "is_active": is_active,
        }
        print(f"New data: {new_data}")

        #TO DO: validation data if
        valid_data = True
        if valid_data:
            updated_user = update_user(user_id, new_data)
            if updated_user: 
                flash('Used successfully updated','succes')
            else:
                flash('User not found','error')
            return redirect(url_for('users.index'))
        
        roles = list_roles()
        user = get_user(user_id)
        return render_template('users/edit_user.html', user=user, roles=roles, new_data=new_data)
    except:
        traceback.print_exc()
        return abort(400)