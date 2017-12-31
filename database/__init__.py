import os

from app import db

def read_text(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def do_query_fetchall(name, params):
    path = os.path.join(os.path.dirname(__file__), 'queries/{}.sql'.format(name))
    return db.session.execute(read_text(path), params).fetchall()

def do_query_fetchone(name, params):
    path = os.path.join(os.path.dirname(__file__), 'queries/{}.sql'.format(name))
    return db.session.execute(read_text(path), params).fetchone()