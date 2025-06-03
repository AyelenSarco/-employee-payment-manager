from flask import Blueprint, render_template,redirect,url_for, request, abort, flash
from src.core.service.service_employee import create_employee, update_employee, get_employee,list_employees, delete_employee
from src.web.handlers.auth import login_required,check
from src.core.schemas.employee import EmployeeCreate, EmployeeUpdate
from pydantic import ValidationError
import traceback

bp = Blueprint("employees", __name__, url_prefix="/employees")

@bp.get("/")
@login_required
@check("employee_list")
def index():
    try:
        pag = request.args.get('pag',1, type = int)
        email = request.args.get('email', type = str)
        if email: 
            email = email.strip()
        name = request.args.get('name', type = str)
        dni = request.args.get('dni', type = str)
        sort_by = request.args.get('sort_by','name')
        sort_order = request.args.get('sort_order','asc')
        
        employees = list_employees(email, name, dni, sort_by,sort_order,pag)

        return render_template('employees/index.html', employees=employees)
    
    except:
        traceback.print_exc()
        return abort(400)
    

@bp.get("/new")
@login_required
@check("employee_create")
def create_form():
    try:
        return render_template('employees/create_employee.html')
    except:
        traceback.print_exc()
        return abort(400)
    
@bp.post("/create")
@login_required
@check('employee_create')
def create():
    try:
        data = request.form.to_dict()
        data['is_active'] = 'is_active' in request.form

        valid_data = EmployeeCreate(**data)
        create_employee(**valid_data.model_dump())

        flash('Employee created successsfully','succes')
        return redirect(url_for('employees.index'))

    except ValueError as e:
        for err in e.errors():
            
            flash(f"{err['loc'][0]}: {err['msg']}",'error')
        
        return render_template('users/create_user.html', new_employee=data)
    except:
        traceback.print_exc()
        return abort(400)
    
    
@bp.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
@check("employee_delete")
def delete(employee_id):
    try:
        deleted = delete_employee(employee_id)
        if deleted is True:
            flash('Employeed deleted successfully','succes')
        else:
            flash('Employee not found','error')
        return redirect(url_for('employees.index'))
    except:
        traceback.print_exc()
        return abort(400)
    

@bp.route("/edit/<int:employee_id>")
@login_required
@check('employee_edit')
def edit(employee_id):
    try:
        employee = get_employee(employee_id)
        return render_template('employees/edit_employee.html', employee=employee)
    except:
        traceback.print_exc()
        return abort(400)


@bp.route("/edit/<int:employee_id>", methods= ['POST'])
@login_required
@check('employee_edit')
def update(employee_id):
    try:
        data = request.form.to_dict()
        data['is_active'] = 'is_active' in request.form

        
        valid_employee_data = EmployeeUpdate(**data) 
        updated_e = update_employee(employee_id,valid_employee_data.model_dump())

        if updated_e is not None:
            flash('Employee updated successfully','succes')
            return redirect(url_for('employees.index'))
        else:
            flash('Employee not found','error')

    except ValidationError as e:

        for err in e.errors():
            
            flash(f"{err['loc'][0]}: {err['msg']}",'error')
        
        return render_template('employees/edit_employee.html', employee = data)

    except:
        traceback.print_exc()
        return abort(400)