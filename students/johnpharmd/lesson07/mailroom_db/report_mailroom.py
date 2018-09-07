from peewee import SqliteDatabase
# from peewee import Model
# from peewee import CharField
# from peewee import IntegerField


def report():
    database = SqliteDatabase('mailroom.db')
    database.connect()
    donor_table = database.execute_sql('select * from donor;')
    for donor in donor_table:
        print(donor)
    database.close()


if __name__ == '__main__':
    report()
