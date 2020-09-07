class Config(object):
    #CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_DATABASE_URI="sqlite:///./test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MUSIC_DIR = 'musicfiles'

class Development(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class Testing(Config):
    TESTING = True

class Production(Config):
    FLASK_ENV = 'production'
