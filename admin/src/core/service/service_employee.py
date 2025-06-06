from flask import abort
from src.core.database import db
from src.core.models import Employee

def create_employee(**kwargs):
    try:
        employee = Employee(**kwargs)
        db.session.add(employee)
        db.session.commit()

        return employee
    except:
        db.session.rollback()
        return abort(500)
    
def get_employee(id):
    try:
        employee = Employee.query.get(id)
        return employee
    except:
        abort(500)

def get_employees():
    try:
        return Employee.query.all()
    except:
        return abort(500)

def update_employee(id, new_data):
    try:
        employee = Employee.query.get(id)
        if employee:
            if new_data.get('name'):
                employee.name = new_data['name']
            if new_data.get('email'):
                employee.email = new_data['email']
            if new_data.get('is_active') is not None:
                employee.is_active = new_data['is_active']
        
        
        db.session.commit()

        return employee
    except:
        db.session.rollback()
        abort(500)

def delete_employee(id):
    try:
        employee_db = Employee.query.get(id)
        if employee_db:
            db.session.delete(employee_db)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
        return abort(500)
    


def list_employees(email = None, name = None, dni = None, sort_by = 'name', sort_order = 'asc', pag = 1):
    try:
        employees = Employee.query.filter_by()

        if email and email != '':
            employees = employees.filter(Employee.email.icontains(f'%{email}'))

        if name and name != '':
            employees = employees.filter(Employee.name.icontains(f'%{name}'))
        
        if dni and dni != '':
            employees = employees.filter(Employee.dni.icontains(f'%{dni}'))

       
        if sort_by == 'email':
            employees = employees.order_by(Employee.email.asc()if sort_order == 'asc' else Employee.email.desc())
        else:
            employees = employees.order_by(Employee.name.asc() if sort_order == 'asc' else Employee.name.desc())
            
        
        employees = employees.paginate(page = pag, per_page=2)

        return employees
    except:
        return abort(500)