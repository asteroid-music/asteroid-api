from flask_restful import Resource, marshal_with, reqparse
from flask import g

from rethinkdb import r

from asteroid_flask.controller import song_marshal

new_song_parser = reqparse.RequestParser()
new_song_parser.add_argument('url')


class SongsList(Resource):
    """ REST Resource for Songs lists """ 

    @marshal_with(song_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(
                r.table('music').run(g.get_conn())
            ), 200


    def post(self):
        """ endpoint for adding new song from url in request data """

        try:
            url = new_song_parser.parse_args(strict=True).url
            if url is None:
                raise
        except:
            return { 'message' : 'Bad URL data.' }, 400

        return {'message': url}, 200


class Songs(Resource):
    """ REST Resource for Songs by song name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(
                r.table('music')
                    .filter(lambda doc:
                        doc['song'].match(name)
                    ).run(g.get_conn())
            ), 200


class Artists(Resource):
    """ REST Resource for Songs by artist name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(
                r.table('music')
                    .filter(lambda doc:
                        doc['artist'].match(name)
                    ).run(g.get_conn())
            ), 200


class Albums(Resource):
    """ REST Resource for Songs by album name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(
                r.table('music')
                    .filter(lambda doc:
                        doc['album'].match(name)
                    ).run(g.get_conn())
            ), 200
