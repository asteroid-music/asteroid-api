from rethinkdb import r
from rethinkdb.errors import RqlRuntimeError

from flask import current_app, g
import flask.cli

import click

def _connect_to_database():
    """ establish and return a connection object """
    return r.connect(
        host=current_app.config["RDB_HOST"],
        port=current_app.config["RDB_PORT"]
    )


@click.command("setup")
@flask.cli.with_appcontext
def db_setup():
    """ create tables in database """
    conn = _connect_to_database()
    for table in ["music", "clients", "queue", "history"]:
        try:
            r.table_create(table).run(conn)
        except RqlRuntimeError:
            current_app.logger.warning(f"Table '{table}' already exists.")
        except Exception as e:
            current_app.logger.error(e)
    conn.close()


def get_db_conn():
    """ creates and/or returns conn object stored in g._db_conn """
    if '_db_conn' not in g:
        g._db_conn = _connect_to_database()

    return g._db_conn


def teardown_db(env):
    """ teardown function to remove g._db_conn if exists """
    conn = g.pop('_db_conn', None)
    
    if conn is not None:
        current_app.logger.info("Disconnecting from database.")
        conn.close()


def register_db_to_context():
    """ registers function to retrieve connection in g.get_conn """
    g.get_conn = get_db_conn


def init_app_database(app):
    """ application init to register functions and cli commands """
    app.teardown_appcontext(teardown_db)
    app.cli.add_command(db_setup) # doesn't include @with_appcontext
    app.before_request(register_db_to_context)
