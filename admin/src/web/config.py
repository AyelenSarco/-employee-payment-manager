from os import getenv

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    """
        Production: This project does NOT implement production, but in a real-world environment,
        the code here could include calls to a Vault client or similar to securely load environment variables.
    """
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')

class TestingCongif(Config):
    """
        Testing: Configuration for automated tests, using an isolated database and minimal parameters.
    """
    TESTING = True
    pass

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingCongif,
}