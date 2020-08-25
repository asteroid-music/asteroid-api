from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from asteroid_flask import bp_api

app = Flask(__name__)

# enable CORS for all domains on all routes
CORS(app)

app.config.from_object('config.Development')

app.register_blueprint(bp_api)

if __name__ == '__main__':
	app.run()
