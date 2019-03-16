"""defines database for use in all modules"""

from mailroom.MongoDBDatabaseLayer import MongoDBAccessLayer
from mailroom.SqliteDatabaseLayer import SQLiteAccessLayer

# this defines database to use for application
# this should be only place where database should be changed
# options: sqlite, mongoDb, redis, neo4j

DATABASE_DISPATCH = {'sqlite': SQLiteAccessLayer,
                     'mongoDB':  MongoDBAccessLayer}
database_selector = 'mongoDB'
Database = DATABASE_DISPATCH.get(database_selector)
