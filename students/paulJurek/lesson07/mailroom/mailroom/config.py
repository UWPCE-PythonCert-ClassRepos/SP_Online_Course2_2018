"""defines database for use in all modules"""

from peewee import *

# this defines database to use for application
# this should be only place where database should be changed
# options: sqlite, mongoDb, redis, neo4j
database_selector = 'sqlite'

database_name = 'mailroom.db'
database = SqliteDatabase(database_name)