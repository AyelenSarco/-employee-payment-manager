from flask import Flask
from src.web.config import config
from src.core import database


def create_app(env="development", static_folder=""):

    app = Flask(__name__)
    app.config.from_object(config[env])
    database.init_app(app)

    import src.core.models

    @app.route("/")
    def home():
        return "hola mundo!"
    

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    
    return app
