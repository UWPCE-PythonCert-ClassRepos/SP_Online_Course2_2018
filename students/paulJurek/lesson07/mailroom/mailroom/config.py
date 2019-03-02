"""defines database for use in all modules"""

from peewee import *

# this defines database to use for application
database_name = 'mailroom.db'
database = SqliteDatabase(database_name)