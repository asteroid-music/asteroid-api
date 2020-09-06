from flask import Flask, redirect
from flask_restful import Api
import flask.cli

from asteroid_flask.services import init_database
from asteroid_flask import bp_api

app = Flask(
    __name__, 
    static_url_path='',
    static_folder='web'
)


if app.debug:
    app.config.from_object('config.Development')
else:
    app.config.from_object('config.Production')

app.register_blueprint(bp_api)



# make root redirect
@app.route('/')
def index():
    return redirect('/index.html')

# init databasing
init_database(app)

if __name__ == '__main__':
    app.run()
