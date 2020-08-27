from flask import Blueprint
from flask_restful import Api

from asteroid_flask.controller.songs_controller import Songs, Artists, Albums, SongsList 
from asteroid_flask.controller.queue_controller import QueueList

bp_api = Blueprint('api', __name__)
api = Api(bp_api)

api.add_resource(SongsList, '/music/songs')
api.add_resource(Songs, '/music/songs/<string:song>')
api.add_resource(Artists, '/music/artist/<string:artist>')
api.add_resource(Albums, '/music/album/<string:album>')

api.add_resource(QueueList, '/queue')
# api.add_resource(Queue, '/queue/<string:id>')

# api.add_resource(History, '/history')

# api.add_resource(Client, '/client')
