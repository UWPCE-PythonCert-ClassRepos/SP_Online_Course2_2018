from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

class Pet(Model):
    owner = ForeignKeyField(Person, backref = 'pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db

db.connect()

db.create_tables([Person, Pet])

from datetime import date

uncle_bob = Person(name='Bob', birthday=date(1960,1,15))
uncle_bob.save()