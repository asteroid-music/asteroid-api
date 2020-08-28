from asteroid_flask.services.database import db

class Music(db.Document):
    song = db.StringField()
    duration = db.IntField()
    artist = db.StringField()
    album = db.StringField()
    file = db.StringField(unique=True)
    url = db.StringField(unique=True)
