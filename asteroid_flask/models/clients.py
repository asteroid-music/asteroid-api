from asteroid_flask.services.database import db

class Client(db.Document):
    name = db.StringField()
