"""
    Create database example with Peewee ORM, sqlite and Python

"""

from personjob_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

databased.create_tables([
        Job,
        Person,
        PersonNumKey,
        Department
    ])

logger.info('Add a few people')
jimmy = Person.create(person_name="Jimmy Stewart", lives_in_town="Bedford Falls")
cary = Person.create(person_name="Cary Grant", lives_in_town="Pottersville")
audrey = Person.create(person_name="Audrey Hepburn", lives_in_town="Akron")

logger.info('Create some departments')
dept_A100 = Department.create(
    dept_number="A100",
    dept_name="Charlie's",
    dept_manager="Testing",
    manager=cary)

dept_ABCD = Department.create(
    dept_number="ABCD",
    dept_name="Chumley's",
    dept_manager="Testing2",
    manager=audrey)

logger.info('Give jimmy some work')

Job.create(
    job_name="Courrier",
    start_date="2018-01-01",
    end_date="2018-12-25",
    salary=10000,
    person_employed=jimmy,
    department=dept_A100
)

Job.create(
    job_name="Banker",
    start_date="2017-02-14",
    end_date="2017-10-31",
    salary=20000,
    person_employed=jimmy,
    department=dept_ABCD
)

databased.close()
