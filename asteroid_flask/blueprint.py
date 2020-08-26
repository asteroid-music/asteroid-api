from flask import Blueprint
from flask_restful import Api, Resource

from asteroid_flask.songs import Songs

bp_api = Blueprint('api', __name__)
api = Api(bp_api)

api.add_resource(Songs, '/songs')
