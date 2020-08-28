from flask_restful import Resource, marshal_with, reqparse, marshal

from asteroid_flask.models import Music

from asteroid_flask.controller import song_marshal
from asteroid_flask.services.requester import Requester

new_song_parser = reqparse.RequestParser()
new_song_parser.add_argument('url')


class SongsList(Resource):
    """ REST Resource for Songs lists """ 

    @marshal_with(song_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(Music.objects()), 200


    def post(self):
        """ endpoint for adding new song from url in request data """

        try:
            url = new_song_parser.parse_args(strict=True).url
            if url is None:
                raise
        except:
            return { 'message' : 'Bad URL data.' }, 400
        else:
            req = Requester(url)
            status = req.fetch()
            if status == 'done':
                song = req.song
                return {
                    'message': 'URL OK.', 
                    'song': marshal(song, song_marshal)
                }, 200
            else:
                return {
                    'message': 'Download / Converstion Error',
                    'status': status,
                }, 400


class Songs(Resource):
    """ REST Resource for Songs by song name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(Music.objects(song__match=name)), 200


class Artists(Resource):
    """ REST Resource for Songs by artist name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(Music.object(artist__match=name)), 200


class Albums(Resource):
    """ REST Resource for Songs by album name """ 

    @marshal_with(song_marshal)
    def get(self, name):
        """ returns items in songs database that match song name """
        return list(Music.objects(album__match=name)), 200
