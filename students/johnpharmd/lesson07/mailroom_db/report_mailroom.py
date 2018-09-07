from peewee import SqliteDatabase


def report():
    database = SqliteDatabase('mailroom.db')
    database.connect()
    print('Last Name____Title__Total Donations__Number of Donations')
    donor_table = database.execute_sql('select * from donor;')
    for donor in donor_table:
        print(donor)
    database.close()


if __name__ == '__main__':
    report()
