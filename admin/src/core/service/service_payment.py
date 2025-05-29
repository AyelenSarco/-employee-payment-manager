from flask import abort
from src.core.database import db
from src.core.models import Payment

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
        payment = Payment.query.get(id)
        return payment
    except:
        return abort(500)
    
def delete_payment(id):
    try:
        payment_db = Payment.query.get(id)
        if payment_db:
            db.session.delete(payment_db)
            db.session.commit()
            return True
        return None
    except:
        db.session.rollback()
        return abort(500)
    
def list_payments():
    try:
        payments = Payment.query(Payment).all()
        return payments
    except:
        return abort(500)