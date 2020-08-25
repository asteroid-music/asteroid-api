from flask_restful import Resource, marshal_with, fields

song_marshal = {
	'name': fields.String,
	'sid': fields.Integer
}

class Songs(Resource):
	""" REST Resource for Songs """ 

	@marshal_with(song_marshal)
	def get(self):
		return {'name': 'Hello World', 'sid': 13}, 200
