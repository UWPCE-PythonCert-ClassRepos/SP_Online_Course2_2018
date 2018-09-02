from peewee import *
import pprint

database = SqliteDatabase('pdj.db')
database.connect()
query = database.execute_sql('select * from job;')

pp = pprint.PrettyPrinter(indent=4)
for job in query:
    pp.pprint([job[5], job[1], job[0]])

database.close()
