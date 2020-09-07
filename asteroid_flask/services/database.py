from flask_sqlalchemy import SQLAlchemy
import flask.cli
import click

db = SQLAlchemy()


@click.command("setup")
@flask.cli.with_appcontext
def db_setup():
    """ create tables in database """
    db.create_all()


def init_database(app):
    """ init the database into application context """
    db.init_app(app)
    app.cli.add_command(db_setup) # doesn't include @with_appcontext
