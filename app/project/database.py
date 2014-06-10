"""
project.database

Simple module that connects to mongo database and returns the
connection
"""
from app.project import config
from mongoengine import connect

def db_init():
    """Connect to database and return the connection"""

    return connect('shakuni-db', host=config.MONGO_DBNAME)
