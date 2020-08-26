from flask import Flask, redirect
from flask_restful import Api
from flask_cors import CORS

from asteroid_flask import bp_api

app = Flask(
	__name__, 
	static_url_path='',
	static_folder='web'
)

# enable CORS for all domains on all routes
CORS(app)
app.config.from_object('config.Development')
app.register_blueprint(bp_api)

# make root redirect
@app.route('/')
def index():
	return redirect('/index.html')

if __name__ == '__main__':
	app.run()
