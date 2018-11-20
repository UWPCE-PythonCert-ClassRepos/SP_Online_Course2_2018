import pprint
pp = pprint.PrettyPrinter(width=120)

from create_personjob import *
import logging
__author__ = "Wieslaw Pucilowski"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')


def main():

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                .select(Person.person_name,
                        Job.job_name,
                        Department.department_name,
                        Job.salary,
                        Job.duration,
                        Department.department_manager)
                .join(Job,
                      JOIN.INNER,
                      on=(Person.person_name == Job.person_employed_id)) # joins person -> job
                .join(Department, 
                      JOIN.LEFT_OUTER,
                      on=(Job.job_department_id == Department.department_number)) # joins job -> department
                .objects()
        )
    
        pp.pprint('{:15} | {:25} | {:15} | {:10} | {:10} | {:20}'.format(
                                    'Person',
                                    'Job',
                                    'Department',
                                    'Salary',
                                    'Duration',
                                    'Manager')
                                    )
        pp.pprint('='*110)
        for job in query:
            pp.pprint('{:15} | {:25} | {:15} | {:10} | {:10} | {:20}'.format(
                                            job.person_name,
                                            job.job_name,
                                            job.department_name,
                                            job.salary,
                                            job.duration,
                                            job.department_manager
                                        )
                   )

    except Exception as e:
        logger.info(e)
    finally:
        database.close()


if __name__ == '__main__':
    main()
