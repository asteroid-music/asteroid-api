from flask_restful import Resource, marshal_with, fields, reqparse
from flask import g

from rethinkdb import r

song_marshal = {
    'artist': fields.String,
    'song': fields.String,
    'duration': fields.Float,
    'album': fields.String,
    'id': fields.String
}


new_song_parser = reqparse.RequestParser()
new_song_parser.add_argument('url')


class Songs(Resource):
    """ REST Resource for Songs by song name """ 

    @marshal_with(song_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(
                r.table('songs').run(g.get_conn())
            ), 200


    def put(self):
        """ endpoint for adding new song from url in request data """
        if name is not None:
            return { 'message' : 'Name field not allowed.' }, 405 

        try:
            url = new_song_parser.parse_args(strict=True).url
            if url is None:
                raise
        except:
            return { 'message' : 'Bad URL data.' }, 400

        return {'url': url}, 200
