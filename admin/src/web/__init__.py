from flask import Flask, render_template, url_for
from flask_session import Session
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.controllers.users import bp as users_bp
from src.web.controllers.auth import auth_bp
from src.web.handlers.error import register_error_handlers
from src.web.handlers.auth import have_permission,is_authenticated, login_required

session = Session()

def create_app(env="development", static_folder="../../static"):

    app = Flask(__name__,static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)
    session.init_app(app)

    import src.core.models

    @app.route("/")
    @login_required
    def home():
        return "hola mundo!"
    

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()
    
    return app
