class Config(object):
    CORS_HEADERS = 'Content-Type'
    MONGO_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
        'port': '27017',
        'alias': 'default',
        'timeout': True
    }
    MUSIC_DIR = 'musicfiles'

class Development(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

class Testing(Config):
    TESTING = True

class Production(Config):
    FLASK_ENV = 'production'
