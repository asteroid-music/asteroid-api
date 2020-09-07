from flask_restful import Resource, marshal_with, fields, reqparse

from asteroid_flask.models import Queue, Music
from asteroid_flask.services.database import db

from asteroid_flask.controller import queue_marshal


new_queue_item_parser = reqparse.RequestParser()
new_queue_item_parser.add_argument('id')


class QueueList(Resource):
    """ REST Resource for Song Queue control """ 

    @marshal_with(queue_marshal)
    def get(self):
        """ returns all items in songs database """
        res =  db.session.query(
            Queue, Music
        ).join(Music).all()

        res = list(map(
            lambda i: {**i[1].__dict__, **i[0].__dict__}, 
            res
        ))

        return res, 200


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
        song = Music.query.filter_by(id=_id).first()

        if song is None:
            return { 'message' : 'Failed to find song.' }, 400

        else:
            new_item = Queue(
                song_id = song.id,
                votes = 1
            )

            # if already in queue
            existing = Queue.query.filter_by(id=_id).first()
            if existing:
                # update
                existing.votes += 1
            else:
                # add new
                db.session.add(new_item)

            db.session.commit()
            return { 'message' : 'Song updated/added to queue.' }, 200
