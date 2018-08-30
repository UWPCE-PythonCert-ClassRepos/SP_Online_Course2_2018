from database_ex import *


database = SqliteDatabase('personjob.db')

try:
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Person.select(Person))
    for person in query:
        print(person)

except Exception as e:
    print(f"EXCEPTION {e}")