import psycopg

import click
from flask import current_app, g
import os


def build_connstring():
    user = current_app.config['CHILLER_DB_USER']
    password = current_app.config['CHILLER_DB_PASSWORD']
    host = current_app.config['CHILLER_DB_HOST']
    port = current_app.config['CHILLER_DB_PORT']
    return f"postgres://{user}:{password}@{host}:{port}"

def create_db(db_name):
    conn = psycopg.connect(build_connstring())
    cursor = conn.cursor()
    conn.autocommit = True
    conn.execute(f"create database {db_name}")
    cursor.close()
    conn.close()

def get_db():
    if 'db' not in g:
        cstr = build_connstring()
        name = current_app.config['CHILLER_DB_NAME']
        g.db = psycopg.connect(f"{cstr}/{name}")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    cur = conn.cursor()

    with current_app.open_resource('db/schema.sql') as f:
        cur.execute(f.read().decode('utf8'))
        conn.commit()
        cur.close()



@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
