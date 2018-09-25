"""
This module defines the database model of persons, jobs, and
departments.
"""
import logging
import datetime as dt
import peewee as pw

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

db_name = 'DennisLee.db'
logger.info(f'Import database {db_name}.')
database = pw.SqliteDatabase(db_name)
logger.info('Connecting.\n')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(pw.Model):
    """Define the base model class behind the real models."""
    class Meta:
        """Assign the database connection."""
        database = database


class Person(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.
    """
    logger.info("Defining table: Person.")
    logger.info("Adding person_name primary key field to Person table.")
    person_name = pw.CharField(primary_key=True, max_length=30, null=False)
    logger.info("Adding lives_in_town field to Person table.")
    lives_in_town = pw.CharField(max_length=40)
    logger.info("Adding nickname field to Person table.\n")
    nickname = pw.CharField(max_length=20, null=True)

class Department(BaseModel):
    """
    Defines the department, which contains the department number,
    department name, job name(s), and manager.
    """
    logger.info("Defining table: Department.")
    logger.info("Adding department_name field to Department table.")
    department_name = pw.CharField(max_length=40, null=False)
    logger.info("Adding manager field to Department table.")
    manager = pw.CharField(max_length=30)
    logger.info(
        "Adding department_number primary key field to Department table. "
        "The field has four digits and must start with a letter.\n"
    )
    department_number = pw.CharField(
        primary_key=True,
        max_length=4,
        constraints=[
            pw.Check('length(department_number) >= 4'),
            pw.Check('substr(department_number, 1) >= "A"'),
            pw.Check('substr(department_number, 1) <= "Z"'),
            pw.Check('substr(department_number, 2, 1) >= "0"'),
            pw.Check('substr(department_number, 2, 1) <= "9"'),
            pw.Check('substr(department_number, 3, 1) >= "0"'),
            pw.Check('substr(department_number, 3, 1) <= "9"'),
            pw.Check('substr(department_number, 4, 1) >= "0"'),
            pw.Check('substr(department_number, 4, 1) <= "9"')
        ]
    )

class DeptJobs(BaseModel):
    """
    This class defines DeptJobs, which links each job name to a
    particular department number.
    """
    logger.info("Defining table: DeptJobs.")
    logger.info("Adding job_name primary key field to DeptJobs table.")
    job_name = pw.CharField(primary_key=True, max_length=30, null=False)
    logger.info(
        "Adding department_number foreign key field to DeptJobs table.\n")
    department_number = pw.ForeignKeyField(Department)

class Job(BaseModel):
    """
    This class defines Job, which maintains details of past Jobs
    held by a Person.
    """
    logger.info("Defining table: Job.")
    logger.info("Adding job_name field to Job table.")
    job_name = pw.ForeignKeyField(DeptJobs)
    logger.info("Adding start_date field to Job table.")
    start_date = pw.DateField(formats='YYYY-MM-DD', null=False)
    logger.info("Adding end_date field to Job table; default is current date.")
    end_date = pw.DateField(formats='YYYY-MM-DD', default=dt.date.today())
    logger.info("Add salary field to Job table.")
    salary = pw.DecimalField(max_digits=7, decimal_places=2)
    logger.info("Add person_employed field to Job table; the field is "
                "a foreign key from the Person table.")
    person_employed = pw.ForeignKeyField(
        Person, related_name='was_filled_by', null=False)

    class Meta:
        """This class defines a composite key as the primary key."""
        logger.info(
            "Set primary key to combo of person_employed & start_date fields.\n"
        )
        primary_key = pw.CompositeKey('person_employed', 'start_date')
