from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    Initialize the database with the Flask application
    """
    db.init_app(app)
    config(app)

    return app

def config(app):
    
    @app.teardown_appcontext
    def close_session(exception=None):
        """
        Closes the database session when each Flask application request completes.
        """
        db.session.close()

    return app

def reset():
    """Database reset"""
    print("Deleting database...")
    db.drop_all()
    print("Creating new database...")
    db.create_all()
    print("Done.")