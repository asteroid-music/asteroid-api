from flask_restful import fields

song_marshal = {
    'artist': fields.String,
    'song': fields.String,
    'duration': fields.Integer,
    'album': fields.String,
    'id': fields.Integer
}

queue_marshal = {
    **song_marshal,
    'votes': fields.Integer
}
