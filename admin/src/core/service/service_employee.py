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

def edit_employee(id, new_data):
    try:
        employee = Employee.query.get(id)
        if employee:
            if new_data.get('dni'):
                employee.dni = new_data['dni']
            if new_data.get('name'):
                employee.name = new_data['name']
            if new_data.get('email'):
                employee.email = new_data['email']
            if new_data.get('is_active'):
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
        return None
    except:
        db.session.rollback()
        return abort(500)
    

def list_employees():
    try:
        employees = Employee.query(Employee).all()
        return employees
    except:
        return abort(500)

