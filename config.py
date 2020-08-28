class Config(object):
    CORS_HEADERS = 'Content-Type'
    MONGO_SETTINGS = {
        'db': 'asteroid',
        'host': 'localhost',
        'port': '27017'
    }
    MUSIC_DIR = 'musicfiles'

class Development(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class Testing(Config):
    TESTING = True

class Production(Config):
    pass
