from flask import abort
from src.core.database import db
from src.core.models import Payment, Employee

def create_payment(**kwargs):
    try:
        payment = Payment(**kwargs)
        db.session.add(payment)
        db.session.commit()

        return payment
    except:
        db.session.rollback()
        return abort(500)
    
def get_payment(id):
    try:
        payment = db.session.query(Payment,Employee.name, Employee.email, Employee.dni)\
                .outerjoin(Employee, Payment.employee_id == Employee.id)\
                .where(Payment.id == id).first()
        
        payment_obj, employee_name, employee_email, employee_dni = payment

        payment_result = {
                            'id': payment_obj.id,
                            'amount': payment_obj.amount,
                            'date': payment_obj.date,
                            'payment_type': payment_obj.payment_type,
                            'description': payment_obj.description,
                            'employee_id': payment_obj.employee_id,
                            'employee_name': employee_name,
                            'employee_email': employee_email,
                            'employee_dni': employee_dni,
                        }
        
        return payment_result
    except:
        return abort(500)
    
def delete_payment(id):
    try:
        payment_db = Payment.query.get(id)
        
        if payment_db:
            db.session.delete(payment_db)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
        return abort(500)
    
def list_payments(payment_type = None, email_employee = None, dni = None, sort_by = 'date', sort_order = 'asc', pag = 1):
    try:
        payments = db.session.query(Payment,Employee.name, Employee.email, Employee.dni)\
                .outerjoin(Employee, Payment.employee_id == Employee.id)


        if payment_type and payment_type != '':
            payments = payments.filter(Payment.payment_type == payment_type)
            
        if email_employee and email_employee != '':
            payments = payments.filter(Employee.email.icontains(f'%{email_employee}'))

        if dni and dni != '':
            payments = payments.filter(Employee.dni.icontains(f'%{dni}'))

        
        
        if sort_by == 'payment_type':
            payments = payments.order_by(Payment.payment_type.asc() if sort_order == 'asc' else Payment.payment_type.desc())
        else: 
            payments = payments.order_by(Payment.date.asc() if sort_order ==  'asc' else Payment.date.desc())

        pagination = payments.paginate(page = pag, per_page=2)

        items = [ 
            {
                'payment':payment,
                'employee_name':name,
                'employee_email': email,
                'employee_dni': dni,
            }
            for payment, name, email, dni in pagination.items
        ]

        return {
            'payments': items,
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num
        }
    except:
        return abort(500)