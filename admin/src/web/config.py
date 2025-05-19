class Config(object):
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

class TestingCongif(Config):
    pass

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingCongif,
}