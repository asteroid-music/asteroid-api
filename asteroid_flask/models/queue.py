from asteroid_flask.services.database import db

class Queue(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    song_id = db.Column(
        db.Integer,
        db.ForeignKey("music.id"),
        unique=True    
    )
    votes = db.Column(
        db.Integer,
        nullable=False
    )

