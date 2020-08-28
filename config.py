class Config(object):
    CORS_HEADERS = 'Content-Type'
    RDB_HOST = 'localhost'
    RDB_PORT = '28015'
    MUSIC_DIR = 'musicfiles'

class Development(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class Testing(Config):
    TESTING = True

class Production(Config):
    pass
