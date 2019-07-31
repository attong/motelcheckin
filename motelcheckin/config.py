class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY="dev"
    HOST="localhost"
    DATABASE="motel6"
    
class ProductionConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY="dev"