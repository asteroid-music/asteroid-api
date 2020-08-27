from flask_restful import Resource, marshal_with, fields
from flask import g

from rethinkdb import r

song_marshal = {
    'artist': fields.String,
    'song': fields.String
}

class Songs(Resource):
    """ REST Resource for Songs """ 

    @marshal_with(song_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(r.table('songs').run(g.get_conn())), 200
