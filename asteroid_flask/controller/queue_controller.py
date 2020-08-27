from flask_restful import Resource, marshal_with, fields, reqparse
from flask import g

from rethinkdb import r

from asteroid_flask.controller import song_marshal


new_queue_item_parser = reqparse.RequestParser()
new_queue_item_parser.add_argument('id', action='append')


class QueueList(Resource):
    """ REST Resource for Song Queue control """ 

    @marshal_with(song_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(
                r.table('queue').run(g.get_conn())
            ), 200


    def post(self):
        """ endpoint for adding new song from url in request data """

        try:
            _id = new_queue_item_parser.parse_args(strict=True).id
            if _id is None:
                raise
        except:
            return { 'message' : 'Bad body/JSON data.'}, 400

        else:
            response, code = self._add_song_to_queue(_id)
            return response, code


    def _add_song_to_queue(self, _id):
        """ fetches songs from music database and adds to song queue """
        if type(_id) is list:
            query = r.table('music').get_all(_id)
        else:
            query = r.table('music').get(_id)

        song = query.run(g.get_conn())

        if song is None:
            return { 'message' : 'Failed to find song.' }, 400

        else:
            r.table('queue').insert(
                song,
                conflict=self._resolve_conflict
            ).run(g.get_conn())

            return { 'message' : 'Song added to queue.' }, 200

    @staticmethod 
    def _resolve_conflict(_id, old, new):
        """ if song already in queue, increment votes by 1 """
        new["votes"] = 1 + old["votes"]
        return { **new, 'id': _id }

