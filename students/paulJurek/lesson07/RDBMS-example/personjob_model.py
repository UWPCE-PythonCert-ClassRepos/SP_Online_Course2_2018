"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema

"""

from peewee import *


database = SqliteDatabase('personjob.db')


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Department(BaseModel):
    """
        This class defines Depatment, which maintains department information
        related to the job
    """
    department_number = CharField(primary_key=True, max_length=4)
    department_name = CharField(max_length=30)
    department_manager = CharField(max_length=30, null=True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    job_name = CharField(primary_key=True, max_length=30)
    start_date = DateField(null=False)
    end_date = DateField(null=False)
    salary = DecimalField(max_digits=7, decimal_places=2)
    person_employed = ForeignKeyField(Person, related_name='was_filled_by',
                                      null=False)
    department = ForeignKeyField(Department, related_name='was_filled_by',
                                 null=False)

    @property
    def days_in_job(self):
        """returns the time in the job"""
        return (self.end_date - self.start_date).days


database.create_tables([Person, Department, Job])
