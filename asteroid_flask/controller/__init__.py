from flask_restful import fields

song_marshal = {
    'artist': fields.String,
    'song': fields.String,
    'duration': fields.Float,
    'album': fields.String,
    'id': fields.String
}
