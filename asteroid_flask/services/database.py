from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_database(app):
    """ init the database into application context """
    db.init_app(app)
