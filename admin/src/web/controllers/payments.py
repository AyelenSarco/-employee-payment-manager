from flask import Blueprint, render_template,redirect,url_for, request, abort, flash
from src.core.service.service_payment import create_payment, delete_payment, list_payments, get_payment
from src.core.service.service_employee import get_employees
from src.web.handlers.auth import login_required,check
from src.core.schemas.payment import PaymentCreate
from pydantic import ValidationError
import traceback

bp = Blueprint("payments",__name__, url_prefix="/payments")

@bp.get("/")
@login_required
@check("payment_list")
def index():
    try:
        pag = request.args.get('pag',1, type = int)
        payment_type = request.args.get('payment_type', type = str)
        
        email_employee = request.args.get('email_employee', type=str)
        if email_employee: 
            email_employee = email_employee.strip()
        dni = request.args.get('dni', type = str)
        sort_by = request.args.get('sort_by','date')
        sort_order = request.args.get('sort_order','asc')

        payments = list_payments(payment_type, email_employee,dni,sort_by,sort_order,pag)


        return render_template('payments/index.html', items=payments)
    except:
        traceback.print_exc()
        return abort(400)
    
@bp.get("/new")
@login_required
@check("payment_create")
def create_form():
    try:
        employees = get_employees()
        return render_template('payments/create_payment.html', employees=employees)
    except:
        traceback.print_exc()
        return abort(400)
    
@bp.post("/create")
@login_required
@check("payment_create")
def create():
    try:
        data = request.form.to_dict()
        employees= get_employees()
        print(f'{data}')
        valid_data = PaymentCreate(**data)
        create_payment(**valid_data.model_dump())

        flash('Payment created successfyllu','succes')
        return redirect(url_for('payments.index'))
    
    except ValidationError as e:

        for err in e.errors():
            
            flash(f"{err['loc'][0]}: {err['msg']}",'error')
        
        return render_template('payments/create_payment.html', payment = data, employees=employees) 
    except:
        traceback.print_exc()
        return abort()
    
@bp.route('/delete/<int:payment_id>', methods=['POST'])
@login_required
@check('payment_delete')
def delete(payment_id):
    try:
        deleted = delete_payment(payment_id)
        if deleted :
            flash('Payment deleted successfully','succes')
        else:
            flash('Payment not found','error')
        
        return redirect(url_for('payments.index'))
    
    except:
        traceback.print_exc()
        return abort(400)
    
@bp.get('/view/<int:payment_id>')
@login_required
@check("payment_view")
def view_payment(payment_id):
    try:
        payment = get_payment(payment_id)

        return render_template("payments/show_payment.html", payment=payment)
    except:
        traceback.print_exc()
        return abort()
    
