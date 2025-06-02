from flask import Blueprint, session,redirect,url_for,render_template,request,flash
from src.web.handlers.auth import is_authenticated
from src.core.service.service_user import search_user_by_email,validate_password


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/")
def login():
    if is_authenticated(session):
        print('Esta autenticado')
        return redirect(url_for('home'))
    return render_template("auth/login.html")


@auth_bp.post("/login")
def authenticate():
    data = request.form
    user = search_user_by_email(data['email'])
    if not user:
        flash("The user is not registered","error")
        return redirect(url_for("auth.login"))
    if not user.is_active:
        flash("Inactive user","error")
        return redirect(url_for("auth.login"))
    
    correct_password = validate_password(user.id, data['password'])
    if not correct_password:
        flash("Incorrect password","error")
        return redirect(url_for("auth.login"))
    
    session['id'] = user.id
    session['name'] = user.name
    session['email'] = user.email
    session['rol'] = user.rol

    return redirect(url_for("home"))

@auth_bp.get("/logout")
def logout():
    if (session.get("email")):
        del session["email"]
        session.clear()
        flash("Session closed successfully","success")
    else:
        flash("There is no active session", "error")

    return redirect(url_for("auth.login"))