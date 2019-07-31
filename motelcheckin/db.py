import psycopg2

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        host = current_app.config["HOST"]
        dbname = current_app.config["DATABASE"]
        #params = "host='{}' dbname='{}' user=root".format(host, dbname)
        params = "dbname='{}' user=root".format(dbname)
        g.db = psycopg2.connect(params)
    # 'g.db' corresponsds to a DB conn
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        with db.cursor() as cursor:
            data = f.read().decode("utf8")
            cursor.execute(data)
            db.commit()
    with current_app.open_resource("seed.sql") as f:
        with db.cursor() as cursor:
            data = f.read().decode("utf8")
            cursor.execute(data)
            db.commit()


def add_data_db():
    db = get_db()
    with current_app.open_resource("seed.sql") as f:
        with db.cursor() as cursor:
            data = f.read().decode("utf8")
            cursor.execute(data)
            db.commit()

def clear_db():
    db = get_db()
    query = """TRUNCATE TABLE business,conditions, buyers, customers, individual, inventoryclerk,manager, manufacturer,purchases, recall, repair, sales, salesperson, seller, users, vehiclecolor, vehicles, vehicletype, vendor CASCADE;"""
    db.cursor().execute(query)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    click.echo("Initializing the database.")
    init_db()
    click.echo("Initialized the database.")

@click.command("clear-db")
@with_appcontext
def clear_db_command():
    """Clear existing data """
    click.echo("Clearing the database.")
    clear_db()
    click.echo("Cleared the database.")

@click.command("add-data-db")
@with_appcontext
def add_data_db_command():
    """Clear existing data and create new tables."""
    click.echo("Adding data to the database.")
    add_data_db()
    click.echo("Finished adding data to the database.")



def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.config.from_object("config.DevelopmentConfig")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_data_db_command)
    app.cli.add_command(clear_db_command)
