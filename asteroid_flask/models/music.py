from asteroid_flask.services.database import db

class Music(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    song = db.Column(
        db.String(128),
        nullable=False    
    )
    duration = db.Column(
        db.Integer
    )
    file = db.Column(
        db.String(128),
        unique=True
    )
    url = db.Column(
        db.String(128),
        unique=True
    )
    artist = db.Column(
        db.String(128),
        nullable=False
    )
    album = db.Column(
        db.String(128),
        nullable=False
    )
