from flask_restful import Resource, marshal_with, fields, reqparse

from asteroid_flask.models import Queue, Music

from asteroid_flask.controller import queue_marshal


new_queue_item_parser = reqparse.RequestParser()
new_queue_item_parser.add_argument('id')


class QueueList(Resource):
    """ REST Resource for Song Queue control """ 

    @marshal_with(queue_marshal)
    def get(self):
        """ returns all items in songs database """
        return list(Queue.objects()), 200


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
        song = Music.objects(id=_id).first()

        if song is None:
            return { 'message' : 'Failed to find song.' }, 400

        else:
            # there must be a nice way to do this no?
            new_item = Queue(
                song = song.song,
                duration = song.duration,
                artist = song.artist, 
                album = song.album,
                file = song.file,
                url = song.url,
                votes = 1
            )

            # if already in queue
            existing = Queue.objects(file=new_item.file).first()
            if existing:
                # update
                existing.votes += 1
                existing.save()
            else:
                # add new
                new_item.save()

            return { 'message' : 'Song updated/added to queue.' }, 200
